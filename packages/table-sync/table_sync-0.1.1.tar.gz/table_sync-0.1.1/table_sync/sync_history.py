import datetime
from .sync_type import SyncType


class SyncHistory:

    def __init__(self, conf, repository):
        self.conf = conf
        self.repository = repository

    def create_sync_details(self):
        self.__write_table_details()
        return self.repository.get_sync_id()

    def write_partition_sync_details(self, sync_id, cnt, partition=None):
        data = {'sync_id': sync_id or 0, 'partition_name': partition or "", 'count': cnt}
        self.repository.write_to_repo(data=data,
                                      table=f"{self.conf.pgsql_schema}.{self.conf.pgsql_partition_table}")

    def update_status(self, status, id):
        self.repository.update_in_repo(f"{self.conf.pgsql_schema}.{self.conf.pgsql_main_table}", id, "status", status)

    def __write_table_details(self):
        data = {'input_schema': self.conf.oracle_schema, 'input_table': self.conf.oracle_table_link,
                'output_schema': self.conf.hive_schema, 'output_table': self.conf.hive_table,
                'logs_check': self.conf.old_partition_sync == SyncType.LOGS, 'partition_check': self.conf.old_partition_sync == SyncType.COUNT,
                'sync_time': datetime.datetime.now(), 'status': "STARTED"}
        self.repository.write_to_repo(data=data,
                                      table=f"{self.conf.pgsql_schema}.{self.conf.pgsql_main_table}")

    def get_rows_count(self):
        return self.repository.get_rows_count()

    def last_sync_date(self, current_sync_id):
        return self.repository.get_last_sync_date(current_sync_id)
