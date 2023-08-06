from pyspark.sql import functions as f
from .boundaries import Boundaries
import logging
import json
import traceback


class DataImporter:

    def __init__(self, conf, oracle, hive, spark_executor, sync_history):
        self.conf = conf
        self.oracle = oracle
        self.hive = hive
        self.spark_executor = spark_executor
        self.sync_history = sync_history
        self.sync_id = 0
        self.oracle_partitions_to_load = None
        self.oracle_partitions_to_sync = None
        self.oracle_partitions = None

    def activate(self):
        self.sync_id = self.sync_history.create_sync_details()
        self.oracle_partitions = self.oracle.find_partitions(self.conf.selected_partition)
        self.oracle_partitions.sort(reverse=True)
        self.oracle_partitions_to_load = self.oracle_partitions[:self.conf.load_limit_partitions]
        sync_limit = self.conf.sync_limit_partitions or self.conf.load_limit_partitions
        self.oracle_partitions_to_sync = self.oracle_partitions[:sync_limit]
        return self.sync_id, self.oracle_partitions_to_sync

    def dump(self):
        logging.info("### EXECUTING def dump ###")
        try:
            if self.oracle_partitions_to_load:
                self.__partitioning_dump()
            else:
                logging.info("### NO ORACLE PARTITIONS TO LOAD ###")
                logging.info("### START SINGLE MONOLITIC DUMP ###")
                self.single_dump()
            self.sync_history.update_status("SUCCEEDED", self.sync_id)
            logging.info('Import completed')
        except Exception as e:
            logging.error('Failed to sync table: ' + str(e))
            traceback.print_exc()
            self.sync_history.update_status("FAILED", self.sync_id)
            exit(1)

    def __partitioning_dump(self):
        partitions_to_load = self.__find_new_partitions_to_dump()
        for partition in partitions_to_load:
            logging.info('Dumping partition: ' + partition)
            self.single_dump(partition)

    def __find_new_partitions_to_dump(self):
        hive_partitions = self.hive.get_partitions()
        missing_partitions = list(set(self.oracle_partitions_to_load) - set(hive_partitions))
        logging.info('Selected following partitions to dump: ' + str(missing_partitions))
        return missing_partitions

    def single_dump(self, partition=None):
        logging.info("### START SINGLE DUMP ###")
        if self.conf.split_by is not None:
            logging.info("### START SPLITTED DUMP ###")
            self.__splitted_dump(partition)
        else:
            logging.info("### START MONOLITIC DUMP ###")
            self.__monolitic_dump(partition)

    def __splitted_dump(self, partition=None):
        split_boundaries = self.oracle.get_boundaries(partition)
        if not split_boundaries.exists():
            logging.warning("Missing data in table/partition or wrong split column data - skipping load for partition: " + str(partition))
            return
        import_query = self.oracle.create_load_query(partition, split_boundaries.is_date)
        self.__download_data(import_query, split_boundaries, partition)
        logging.info('Data loaded')
        self.hive.sync_table(partition)

    def __monolitic_dump(self, partition=None):
        import_query = self.oracle.create_load_query(partition)
        logging.info("### MONOLITIC DUMP SQL QEURY")
        logging.info(import_query)
        self.__download_data(import_query, Boundaries(), partition)
        logging.info('Data loaded')
        self.hive.sync_table(partition)

    def __download_data(self, query, split_boundaries, partition=None):
        logging.info("### START DATA DOWNLOAD ###")
        df = self.spark_executor.execute_oracle_load_query(query, split_boundaries)
        logging.info(f"The type of cast_columnn is {type(self.conf.cast_columns)}")
        logging.info(f"The cast column is ||{self.conf.cast_columns}||")
        if self.conf.cast_columns and self.conf.cast_columns != 'null':
            try:
                df =  self.__cast_columns(df, json.loads(self.conf.cast_columns))
            except Exception as e:
                logging.info(f"Failed to use cast_colum config")
                logging.info(str(e))
        #todo add support for tables without partitions in oracle but with partitioning on hive
        hdfs_path = self.conf.hive_table_path
        if partition:
            hdfs_path += f'/oraclepartition={partition}/'
        if split_boundaries.is_date:
            df.drop("split_by_date_column")
        self.__write_to_hdfs(df, hdfs_path)
        self.sync_history.write_partition_sync_details(self.sync_id, df.count(), partition)

    def __write_to_hdfs(self, df, path):
        logging.info(f"Writing data to path: {path}")
        if self.conf.repartition_num is not None:
            df = df.repartition(self.conf.repartition_num)
        df.write.parquet(path, mode='overwrite')

    def __cast_columns(self, df, column_types={}):
        for column_name, data_type in column_types.items():
            df = df.withColumn(column_name, f.col(column_name).cast(data_type))
        return df
