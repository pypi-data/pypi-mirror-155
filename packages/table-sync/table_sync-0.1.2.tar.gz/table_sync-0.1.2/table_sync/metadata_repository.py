import psycopg2

connection_parrams=dict(
dbname='synclist',
#host='jdbc:postgresql://master-02.kraken.kcell.kz:5432/synclist',
host="192.168.213.202",
port="5432",
user='synclist',
password='8VgEp674Nrsh'
)

class MetadataRepository:

    def __init__(self, conf):
        self.conf = conf
        # self.conn = psycopg2.connect(dbname=self.conf.pgsql_dbname, host=self.conf.pgsql_url,
        #                              user=self.conf.pgsql_user, password=self.conf.pgsql_password)
        self.conn = psycopg2.connect(**connection_parrams)
        self.cur = self.conn.cursor()

    def __exit__(self):
        self.cur.close()
        self.conn.close()

    def write_to_repo(self, data, table):
        columns = ", ".join(data.keys())
        params = ", ".join(['%s' for i in range(len(data))])
        query = f"insert into {table} ({columns}) values ({params})"
        self.cur.execute(query, list(data.values()))
        self.conn.commit()

    def get_last_sync_date(self, current_sync_id):
        query = self.__create_query_for_last_sync_date(current_sync_id)
        result = self.__execute_query(query)
        return self.__get_result_safely(result, 0)

    def get_rows_count(self):
        query = self.__create_query_for_rows_count()
        result = self.__execute_query(query)

        out = {}
        if result:
            for row in result:
                out[row[1]] = row[0]
        return out

    def get_sync_id(self):
        query = self.__create_query_for_sync_id()
        result = self.__execute_query(query)
        return self.__get_result_safely(result, 0)

    def update_in_repo(self, table, id, column, value):
        query = f"UPDATE {table} set {column} = %s where id = %s"
        self.cur.execute(query, (value, id,))
        self.conn.commit()

    def __create_query_for_sync_id(self):
        query = f'''
        select max(id) id from {self.conf.pgsql_schema}.{self.conf.pgsql_main_table}
        where input_schema = '{self.conf.oracle_schema}' and input_table = '{self.conf.oracle_table_link}'
        and output_schema = '{self.conf.hive_schema}' and output_table = '{self.conf.hive_table}'
        '''
        return query

    def __create_query_for_rows_count(self):
        query = f'''
        select max("count") as cnt, partition_name from 
            {self.conf.pgsql_schema}.{self.conf.pgsql_partition_table} partition
        join {self.conf.pgsql_schema}.{self.conf.pgsql_main_table} main
        on (main.id = partition.sync_id)
        where input_schema = '{self.conf.oracle_schema}' and input_table = '{self.conf.oracle_table_link}'
        and output_schema = '{self.conf.hive_schema}' and output_table = '{self.conf.hive_table}'
        and status = 'SUCCEEDED'
        group by partition_name'''
        return query

    def __create_query_for_last_sync_date(self, current_sync_id):
        query = f'''
        select max(sync_time) sync_time 
        from {self.conf.pgsql_schema}.{self.conf.pgsql_main_table}
        where input_schema = '{self.conf.oracle_schema}' and input_table = '{self.conf.oracle_table_link}'
        and output_schema = '{self.conf.hive_schema}' and output_table = '{self.conf.hive_table}'
        and logs_check = TRUE and id != {current_sync_id} and status = 'SUCCEEDED'
        '''
        return query

    def __execute_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    @staticmethod
    def __get_result_safely(result, id):
        return result[0][id] if result else None
