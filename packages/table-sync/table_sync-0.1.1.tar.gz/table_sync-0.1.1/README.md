# Table sync

## Configuration

```bash
--oracle_config_path
    path to the file with oracle configuation
--pg_config_path
    path to the file with postgress config
--oracle_schema 
--oracle_table
--oracle_link
    source of data in oracle
--hive_schema
--hive_table
--hive_table_path
    data destination in hive
--spark_config
    spark configuration
--split_by
    column to split data by
--split_partitions_number
    number of partitions/chunks that the whole range of values in selected column (split_by) will be divided into 
--load_limit_partitions
    limitation of partitions to be loaded if not exists
--sync_limit_partitions
    limitation of partitions to be sync (if already loaded)
--cast_columns
    data types to cast 
```

### Flags used for sync history
```bash
--old_partition_sync
    how to synchronize partitions, options:
        NONE (default),
        COUNT - compare number of rows in partitions,
        LOGS - check logs in <history_log_table>
--history_log_table
    name of the table with changes history: dwh_adm.dwh_fct_summary_log
--tracked_table
    name of table tracked in <history_log_table>, default: <oracle_table>
--pg_config_path
    path to json file with postgres config
--oracle_config_path
    path to json file with oracle config
```
### Sample postgres config
```
{
  "pgsql_url": "master-02.kraken.kcell.kz",
  "pgsql_dbname": "synclist",
  "pgsql_user": "synclist",
  "pgsql_password": "<password>",
  "pgsql_schema": "sync_history",
  "pgsql_main_table": "main_history",
  "pgsql_partition_table": "partition_details",
}
```

### Sample oracle config
```
{
  "oracle_jdbc_url": "jdbc:oracle:thin:@dm01-scan.kcell.kz:1521/acrm",
  "oracle_user": "app_dl",
  "oracle_password": "<password>",
  "oracle_jdbc_opetions": "{\"fetchsize\": \"5000\"}"
}
```

### Managing oracle/postgress configuration as secrets in oracle




## Running integration tests 

    ./run-tests.sh
