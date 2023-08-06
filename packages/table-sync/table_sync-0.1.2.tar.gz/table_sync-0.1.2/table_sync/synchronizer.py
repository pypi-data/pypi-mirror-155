import logging


class Synchronizer:
    def load(self, oracle, sync_history, hive, sync_id, data_importer, oracle_partitions):
        self.oracle = oracle
        self.sync_history = sync_history
        self.hive = hive
        self.current_sync_id = sync_id
        self.data_importer = data_importer
        self.oracle_partitions = oracle_partitions

    def synchronize(self):
        pass


class CountSynchronizer(Synchronizer):
    def synchronize(self):
        try:
            hive_partitions = self.hive.get_partitions()
        except Exception as e: 
            logging.info("Failed to get hive partitions")
            logging.info(str(e))
            hive_partitions = []
            logging.info("NOT USING HIVE PARTITIONS")
        
        common_partitions = list(set(self.oracle_partitions).intersection(hive_partitions))
        if common_partitions:
            rows_count = self.sync_history.get_rows_count()
            oracle_rows_count = self.oracle.get_rows_count(common_partitions)

            for partition in common_partitions:
                last_oracle_rows_count = oracle_rows_count[partition] if partition in oracle_rows_count else 0
                last_rows_count = rows_count[partition] if partition in rows_count else 0
                if last_oracle_rows_count > last_rows_count:
                    logging.info(f"sync old partition: {partition}")
                    self.data_importer.single_dump(partition)
        if len(common_partitions) == 0:
            logging.info("### NO PARTITIONS ARE AVAILABLE ###")


class LogsSychronizer(Synchronizer):
    def synchronize(self):
        last_sync_date = self.sync_history.last_sync_date(self.current_sync_id)
        if last_sync_date:
            changed_partitions = self.oracle.get_changed_partitions(last_sync_date)
            for changed_partition in changed_partitions:
                logging.info(f"partition {changed_partition['PARTITION']} updated")
                self.data_importer.single_dump(changed_partition['PARTITION'])