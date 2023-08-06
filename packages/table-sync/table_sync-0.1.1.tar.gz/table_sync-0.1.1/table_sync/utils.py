# from ast import arg
import os
import argparse
import json
import logging
import sys
print(sys.version)
print(sys.path)
try:
    from .sync_type import SyncType
except ImportError as e:
    logging.info("Failed to import SyncType from .sync_type")
    logging.info(str(e))
    from sync_type import SyncType
    assert SyncType


try:
    from .synchronizer import CountSynchronizer, LogsSychronizer, Synchronizer
except ImportError as e:
    logging.info("Failed to import  from .synchronizer")
    logging.info(str(e))
    from synchronizer import CountSynchronizer, LogsSychronizer, Synchronizer
    assert LogsSychronizer
    assert CountSynchronizer
    assert Synchronizer

def print_detailed_exception_info():
            import os, sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info(exc_type, fname, exc_tb.tb_lineno, exc_obj)

# def pretty_print_dict(args: dict):
#     import json
#     logging.info(json.dumps(args,  sort_keys=True, indent=4))


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def process_arguments():
        # TODO: extra arg to choose oracle schema accounnt, i.e.
        # dwh -> app_cbm account
        try:
            args = Utils.parse_arguments()
        except Exception as e:
            logging.info("Failed to parse args")
            print_detailed_exception_info()
            # pass
        try:
            args = Utils.load_json_to_conf(args, args.pg_config_path)
            # pass
        except Exception as e:
            logging.info(
                "Failed to parse pg_config_path, using the default value")
            # with open(path) as json_file:
            # data = json.load(json_file)
            data = {
                "url": "jdbc:postgresql://master-02.kraken.kcell.kz:5432/synclist",
                "username": "synclist",
                "password": "8VgEp674Nrsh",
                "pgsql_dbname": "synclist",
                "pgsql_schema": "sync_history",
                "pgsql_main_table": "main_history",
                "pgsql_partition_table": "partition_details"
            }
            for k, v in data.items():
                args.__dict__[k] = v
            logging.info(str(e))

            args = Utils.load_json_to_conf(
                args,  "/home/airflow/pg_config.json")
        try:
            args = Utils.load_json_to_conf(args, args.oracle_config_path)
            assert args is not None, "args is None at line 62"
        except Exception as e:
            logging.info(
                "Failed to parse oracle_config_path, using the default value")
            logging.info(str(e))
            import os, sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info(exc_type, fname, exc_tb.tb_lineno, exc_obj)
            args = Utils.load_json_to_conf(
                args,  "/home/airflow/oracle_config.json")
            assert args is not None
        args = Utils.prepare_table_with_link(args)
        return args
# /opt/miniconda3/envs/airflow_env/bin/python3 -m table_sync
# --oracle_config_path oracle-conf.json
# --pg_config_path sync-postgresql-conf.json
# --oracle_schema dwh
# --oracle_table dim_kpss_sales_scheme
# --hive_schema oracle_sync
# --hive_table dim_kpss_sales_scheme
# --hive_table_path /warehouse/tablespace/managed/hive/oracle_sync.db/dim_kpss_sales_scheme
# --spark_config '{spark.dynamicAllocation.maxExecutors:' 1, spark.dynamicAllocation.minExecutors: 1, spark.dynamicAllocation.initialExecutors: 1, spark.executor.cores: 1, spark.executor.memory: 3g, spark.driver.memory: '1g}'
# --cast_columns '{kpss_sales_scheme_id:' Integer, source_key: 'Integer}'

    @staticmethod
    def parse_arguments():
        logging.info(
            "Preparing arguments for dump"
        )
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--oracle_config_path",
            required=False,
            default=(
                "/home/airflow/"
                "tables_sync/scheduling/config/oracle_accounts.json"
            )
        )
        assert parser is not None
        # parser.add_argument("--pg_config_path", required=True,
        #                     default="/home/airflow/pg_config.json")
        parser.add_argument("--oracle_schema", required=True, default='dwh')
        parser.add_argument("--oracle_table", required=True,
                            default='dim_kpss_sales_scheme')
        parser.add_argument("--oracle_link", required=False, default=None)
        parser.add_argument("--spark_config", required=True)
        # ,
        #         default='''{
        #         "spark.dynamicAllocation.maxExecutors": "1",
        #         "spark.dynamicAllocation.minExecutors": "1",
        #         "spark.dynamicAllocation.initialExecutors": "1",
        #         "spark.executor.cores": "1",
        #         "spark.executor.memory": "3g",
        #         "spark.driver.memory": "1g"
        #         }''', action='store_true')
        parser.add_argument("--selected_partition", required=False)
        parser.add_argument("--hive_schema", required=True,
                            default='oracle_sync')
        parser.add_argument("--hive_table", required=True,
                            default='dim_kpss_sales_scheme')
        parser.add_argument(
            "--hive_table_path",
            required=True,
            default=(
                "/warehouse/tablespace/"
                "managed/hive/oracle_sync.db/dim_kpss_sales_scheme"
            )
        )
        parser.add_argument(
            "--cast_columns",
            required=True,
            default=(
                "{\"kpss_sales_scheme_id\": \"Integer\", "
                "\"source_key\": \"Integer\"}"
            )
        )
        parser.add_argument("--split_by", required=False)
        parser.add_argument("--split_partitions_number",
                            required=False, default=30, type=int)
        parser.add_argument("--load_limit_partitions",
                            required=False, default=12, type=int)
        parser.add_argument("--sync_limit_partitions",
                            required=False, default=None, type=int)
        parser.add_argument("--repartition_num",
                            required=False, default=None, type=int)
        parser.add_argument("--old_partition_sync", required=False,
                            default=SyncType.NONE,
                            type=SyncType.from_string, choices=list(SyncType))
        # parser.add_argument("--history_log_table", required=False, type=str)
        # parser.add_argument("--tracked_table", required=False)
        parsed_args, _ = parser.parse_known_args()
        # logging.info(f"£££ ### the parsed args are {parsed_args}")
        # logging.info(f"args is {parsed_args.__dict__}")
        logging.info(parsed_args.__dict__)
        return parsed_args

    @staticmethod
    def load_json_to_conf(
        args,
        path
    ):
        # logging.info("IN LOAD_JSON_TO_CONF")
        # logging.info(f"args is {args}")
        # logging.info(f"path is {path}")
        with open(path) as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                args.__dict__[k] = v
        return args

    @staticmethod
    def prepare_table_with_link(args):
        if args.oracle_link:
            args.__dict__["oracle_table_link"] = args.oracle_table + \
                '@' + args.oracle_link
        else:
            args.__dict__["oracle_table_link"] = args.oracle_table
        return args

    @staticmethod
    def configure_logger():
        logging.basicConfig(format="%(asctime)s %(message)s")
        logging.getLogger().setLevel(logging.INFO)

    @staticmethod
    def create_strategy(sync_type):
        if sync_type == SyncType.LOGS:
            return LogsSychronizer()
        if sync_type == SyncType.COUNT:
            return CountSynchronizer()
        return Synchronizer()


# cur_dir = os.environ.get("HOME", "./")
# default_path = (
#     f"{cur_dir}/tables_sync/scheduling/config/"
#     "oracle_account.json"
# )

def create_temp_args():
    parser = argparse.ArgumentParser()
    args = parser.add_argument(
        "--oracle_config_path",
        required=False
        # default=default_path
        )
    parser.add_argument("--oracle_schema", required=False, default='dwh')
    # spark_config =  {
    #   "spark.dynamicAllocation.maxExecutors": "50",
    #   "spark.dynamicAllocation.minExecutors": "25",
    #   "spark.dynamicAllocation.initialExecutors": "25",
    #   "spark.executor.cores": "2",
    #   "spark.executor.memory": "16g",
    #   "spark.driver.memory": "6g"
    # }
    args = parser.parse_args()
    oracle_config_path = "scheduing/config/oracle_accounts.json"
    args = Utils.load_json_to_conf(args, args.oracle_config_path)
    assert args is not None
    assert 'app_cbm' in args.__dict__
    assert set(args.__dict__['app_cbm'].keys()) == {
        'oracle_user', 'oracle_password', 'oracle_jdbc_options', 'oracle_jdbc_url'}
    map_schemas_to_accounts = {
        "dwh": "app_cbm"
    }
    # args.__dict__['oracle_table'] = "dim_service"
    args.__dict__['oracle_table'] = "FCT_REFILL"
    args.__dict__['oracle_link'] = "acrm_lk01.kcell.kz"
    oracle_schema = args.__dict__['oracle_schema']
    oracle_account = map_schemas_to_accounts[oracle_schema]
    oracle_account_details = args.__dict__[oracle_account]
    args.__dict__.update(oracle_account_details)    
    del args.__dict__[oracle_account]
    args.__dict__['spark_config'] = "/home/airflow/tables_sync/scheduling/config/spark_config.json"
    # args.__dict__['oracle_table_link'] = 
    logging.info("### TEMP ARGS FOR DWH.FCT_REFILL ###")
    logging.info(str(args))
    return args

# import json
# args = create_temp_args()
# spark_config = json.loads(args.spark_config)
# print("done")