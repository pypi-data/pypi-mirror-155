import logging


class Hive:

    def __init__(self, conf, spark_executor):
        self.spark_executor = spark_executor
        self.conf = conf
        self.partitions = None

    def get_partitions(self):
        if not self.partitions:
            self.partitions = self.__load_partitions()
        return self.partitions

    def __load_partitions(self):
        if not self.__table_exists(self.conf.hive_table, self.conf.hive_schema):
            return []
        query = f"SHOW PARTITIONS {self.conf.hive_schema}.{self.conf.hive_table}"
        query = f"SHOW PARTITIONS {self.conf.hive_schema}.{self.conf.hive_table}"
        logging.info("executing HIVE SQL\n")
        logging.info(query)

        partitions_result = self.spark_executor.execute_hive_query(query)
        partitions_key_value = [row['partition'] for row in partitions_result]
        partitions = [row.split("=")[1] for row in partitions_key_value]
        logging.info('Found following partitions in hive: ' + str(partitions))
        return partitions

    def sync_table(self, is_partitioned):
        if not self.__table_exists(self.conf.hive_table, self.conf.hive_schema):
            logging.info(f'''Table {self.conf.hive_table} doesn't exist, creating new table in {self.conf.hive_schema} ({self.conf.hive_table_path})''')
            self.__create_table(self.conf.hive_table, self.conf.hive_schema, self.conf.hive_table_path)
            logging.info('Table created')
        if is_partitioned:
            logging.info('Recovering partitions')
            self.__recover_partitions(self.conf.hive_table, self.conf.hive_schema)
            logging.info('Partitions recovered')

    def __table_exists(self, table, database):
        tables = [table.name for table in self.spark_executor.get_catalog().listTables(database)]
        logging.info(f'''Found following tables: {tables}''')
        return table.lower() in tables

    def __create_table(self, table, database, path):
        self.spark_executor.get_catalog().createExternalTable(f'{database}.{table}', path=path)

    def __recover_partitions(self, table, database):
        self.spark_executor.get_catalog().recoverPartitions(f'{database}.{table}')

