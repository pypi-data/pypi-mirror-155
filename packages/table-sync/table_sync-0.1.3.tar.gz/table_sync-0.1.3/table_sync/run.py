import logging
try:
    from .utils import Utils
except ImportError:
    from utils import Utils

try:
    from .spark_executor import SparkExecutor
except ImportError:
    from spark_executor import SparkExecutor

try:
    from .data_importer import DataImporter
except ImportError:
    from data_importer import DataImporter

try:
    from .oracle import Oracle
except ImportError:
    from oracle import Oracle

try:
    from .hive import Hive
except ImportError:
    from hive import Hive

try:
    from .sync_history import SyncHistory
except ImportError:
    from sync_history import SyncHistory

try:
    from .metadata_repository import MetadataRepository
except ImportError:
    from metadata_repository import MetadataRepository


def run():
    Utils.configure_logger()
    args = Utils.process_arguments()
    spark_executor = SparkExecutor(args)
    repository = MetadataRepository(args)
    sync_history = SyncHistory(args, repository)
    oracle = Oracle(args, spark_executor)
    hive = Hive(args, spark_executor)
    data_importer = (DataImporter(
        args,
        oracle,
        hive,
        spark_executor,
        sync_history))
    logging.info("### GETTING ORACLE PARTITIONS START ###")
    sync_id, partitions = data_importer.activate()
    logging.info("### GETTING ORACLE PARTITIONS END ###")
    synchronizer = Utils.create_strategy(args.old_partition_sync)
    synchronizer.load(oracle, sync_history, hive, sync_id, data_importer, partitions)
    logging.info("### SYNCHRONIZER INIT LOAD END ###")
    try:
        synchronizer.synchronize()
    except Exception as e:
        logging.info("Failed to sync partitions")
        logging.info("{str(e)}")
    logging.info("### START DATA IMPORT ###")
    data_importer.dump()
