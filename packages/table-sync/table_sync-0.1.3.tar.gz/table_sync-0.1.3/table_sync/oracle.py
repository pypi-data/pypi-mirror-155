import logging
from .boundaries import Boundaries


class Oracle:

    def __init__(self, conf, spark_executor):
        self.conf = conf
        self.spark_executor = spark_executor
        self.partitions = None

    def create_load_query(self, partition=None, bound_is_date=False):
        split_by_date_column = ""
        if bound_is_date:
            split_by_date_column = f"CAST({self.conf.split_by} as TIMESTAMP) split_by_date_column,"
        query = f"select {split_by_date_column} a_.* from {self.conf.oracle_schema}.{self.conf.oracle_table_link} "
        if partition is not None:
            query += f"PARTITION ({partition}) "
        query += "a_ "
        return query

    def find_partitions(self, selected_partition):
        if not self.partitions:
            self.partitions = self.__load_partitions(selected_partition)
        return self.partitions

    def __load_partitions(self, selected_partition):
        # todo consider links to external DBs if there is any table with partitioning there
        query = self.__create_query_for_partitions(selected_partition)
        partitions_result = self.spark_executor.execute_oracle_query(query).collect()
        partitions = [row['PARTITION_NAME'] for row in partitions_result]
        logging.info('Found following partitions in oracle: ' + str(partitions))
        return partitions

    def __create_query_for_partitions(self, selected_partition):
        if self.conf.oracle_link:
            query = f'''
            select PARTITION_NAME 
            from ALL_TAB_PARTITIONS@{self.conf.oracle_link}
            where lower(TABLE_OWNER) = lower('{self.conf.oracle_schema}') 
            and lower(TABLE_NAME) = lower('{self.conf.oracle_table}') 
            and PARTITION_NAME not like 'SYS_%'             
            '''
        else:
            query = f'''
            select PARTITION_NAME 
            from ALL_TAB_PARTITIONS 
            where lower(TABLE_OWNER) = lower('{self.conf.oracle_schema}') 
            and lower(TABLE_NAME) = lower('{self.conf.oracle_table}') 
            and PARTITION_NAME not like 'SYS_%'             
            '''

        if selected_partition:
            query += f" and lower(PARTITION_NAME) = lower('{selected_partition}')"
        query += " order by PARTITION_NAME DESC"
        return query

    def get_boundaries(self, partition=None):
        is_date = self.__is_date_type(self.conf.split_by, self.conf.oracle_table)
        bounds_query = self.create_query_for_boundaries(is_date, partition)
        boundaries = self.spark_executor.execute_oracle_query(bounds_query).collect()
        lower_bound = boundaries[0]['LOWER_BOUND']
        upper_bound = boundaries[0]['UPPER_BOUND']
        logging.info(f'Lower bound for partitioning: {lower_bound}, upper bound: {upper_bound}')
        return Boundaries(lower_bound, upper_bound, is_date)

    def create_query_for_boundaries(self, is_date, partition):
        if is_date:
            agg_columns = [
                f'''to_char(min(cast({self.conf.split_by} as TIMESTAMP)), 'yyyy-mm-dd hh24:mi:ss.FF') as LOWER_BOUND''',
                f'''to_char(max(cast({self.conf.split_by} as TIMESTAMP)), 'yyyy-mm-dd hh24:mi:ss.FF') as UPPER_BOUND''']
        else:
            agg_columns = [f'''min({self.conf.split_by}) as LOWER_BOUND''',
                           f'''max({self.conf.split_by}) as UPPER_BOUND''']
        bounds_query = f"select {','.join(agg_columns)} from {self.conf.oracle_schema}.{self.conf.oracle_table_link}"
        if partition:
            bounds_query += f" PARTITION ({partition})"
        return bounds_query

    def __is_date_type(self, column_name, table_name):
        metadata_table_name = 'all_tab_columns'
        if self.conf.oracle_link:
            metadata_table_name = metadata_table_name + '@' + self.conf.oracle_link
        query = f''' select data_type from {metadata_table_name} where table_name='{table_name.upper()}' and column_name='{column_name.upper()}' '''
        column_type = self.spark_executor.execute_oracle_query(query).collect()[0]['DATA_TYPE']
        date_types = ['DATE', 'TIMESTAMP']
        if any(date_type in column_type for date_type in date_types):
            return True
        return False

    def get_rows_count(self, partitions):
        query = " UNION ALL ".join([self.__get_count_query_for_partition(partition) for partition in partitions])
        result = self.spark_executor.execute_oracle_query(query)

        out = {}
        if result:
            for row in result.collect():
                out[row["PARTITION_NAME"]] = row["CNT"]
        return out

    def __get_count_query_for_partition(self, partition):
        query = f'''select '{partition}' as partition_name, count(*) as cnt
        from {self.conf.oracle_schema}.{self.conf.oracle_table_link} partition ({partition})'''
        return query

    def get_changed_partitions(self, begin_date):
        tracked_table = self.conf.tracked_table or f"{self.conf.oracle_table}"
        query = self.__create_query_for_history(begin_date, tracked_table)
        return self.spark_executor.execute_oracle_query(query).collect()

    def __create_query_for_history(self, begin_date, tracked_table):
        query = f'''select distinct 'P'|| to_char(loaded_days, 'yyyymmdd') as partition  from {self.conf.history_log_table}
        where lower(fact_table) = lower('{tracked_table}')
        and commit_timestamp$ > TO_TIMESTAMP('{begin_date}', 'YYYY-MM-DD HH24:MI:SS.FF') '''
        return query

