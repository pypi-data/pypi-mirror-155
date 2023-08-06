import logging
import json
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf


class SparkExecutor:

    def __init__(self, conf):
        self.conf = conf
        spark_config = json.loads(conf.spark_config)
        logging.info(f"spark_config={spark_config}")
        config = [(key, value) for key, value in spark_config.items()]
        sconf = SparkConf().setAppName('oracle_import').setAll(config)
        logging.info('Launching spark session')
        self.spark = SparkSession.builder.config(conf=sconf).enableHiveSupport().getOrCreate()
        application_id =self. spark._jsc.sc().applicationId()
        tracking_url = f"http://master-02.kraken.kcell.kz:8088/proxy/{application_id}/"
        logging.info(
                f"""<a href="{tracking_url}">link to application tracking: {application_id}</a>""")

    def get_catalog(self):
        return self.spark.catalog

    def __get_oracle_spark(self, query, options={}):
        logging.info(f'Executing query: {query}')
        # self.conf.oracle_user = "app_cbm"
        # self.conf.oracle_password = "Wrt43xpZ5#"
        # self.conf.oracle_jdbc_url = "jdbc:oracle:thin:@mddbrep-pmy.kcell.kz:1521/MDDBREP.KCELL.KZ"
        # cx_Oracle.connect('app_mmp/jlkjl_34jcfds@acrm-pmy.kcell.kz/acrm', encoding='UTF-8')
        self.conf.oracle_user = "app_mmp"
        self.conf.oracle_password = "jlkjl_34jcfds"
        # self.conf.oracle_jdbc_url = "acrm-pmy.kcell.kz:1521/acrm"
        self.conf.oracle_jdbc_url = "jdbc:oracle:thin:@(description=(address=(protocol=tcp)(host=acrm-pmy)(port=1521))(connect_data=(service_name=acrm)))"

        logging.info("### USING FOLLOWING ORACLE ACCOUNT### ")
        logging.info(f"conf.oracle_user={self.conf.oracle_user}")
        logging.info(f"conf.oracle_password={self.conf.oracle_password}")
        logging.info(f"conf.oracle_jdbc_url={self.conf.oracle_jdbc_url}")
        logging.info(f"USING ORACLE SQL={query}")
        return (self.spark.read
                .format("jdbc")
                .option("driver", "oracle.jdbc.OracleDriver")
                .option("url", self.conf.oracle_jdbc_url)
                .option("user", self.conf.oracle_user)
                .option("password", self.conf.oracle_password)
                .option("dbtable", f'({query}) qry')
                .options(**options))

    def execute_oracle_load_query(self, query, split_boundaries):
        spark = self.__get_oracle_spark(query, json.loads(self.conf.oracle_jdbc_options))
        if split_boundaries.exists():
            spark = (spark.option("partitionColumn", ("split_by_date_column" if split_boundaries.is_date else self.conf.split_by))
                          .option("lowerBound", split_boundaries.lower_bound)
                          .option("upperBound", split_boundaries.upper_bound)
                          .option("numPartitions", self.conf.split_partitions_number)
                          .option("oracle.jdbc.mapDateToTimestamp", "false")
                          .option("sessionInitStatement", "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS''")
                          .option("sessionInitStatement", "ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'"))
        return spark.load()

    def execute_oracle_query(self, query):
        logging.info(f"executing SQL oracle query: {query}")
        return self.__get_oracle_spark(query, json.loads(self.conf.oracle_jdbc_options)).load()

    def execute_hive_query(self, query):
        return self.spark.sql(query).collect()

    def to_dataframe(self, list_of_dicts):
        return self.spark.createDataFrame(Row(**x) for x in list_of_dicts)
