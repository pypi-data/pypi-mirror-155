from dacite import from_dict
from datetime import datetime
import json
from dacite import from_dict
from os.path import join
import logging

from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.exceptions import AirflowException
from airflow.operators.bash import BashOperator

from gcp_airflow_foundations.operators.api.sensors.gcs_sensor import GCSObjectListExistenceSensor
from gcp_airflow_foundations.operators.api.sensors.gcs_prefix_sensor import GCSObjectPrefixListExistenceSensor
from gcp_airflow_foundations.source_class.generic_file_source import GenericFileIngestionDagBuilder
from gcp_airflow_foundations.base_class.file_source_config import FileSourceConfig


class GCSFileIngestionDagBuilder(GenericFileIngestionDagBuilder):
    """
    Builds DAGs to load files from GCS to a BigQuery Table.

    For GCS->BQ ingestion, either a metadata file is required or the field templated_file_name must be provided.
    If a metadata file is provided, itt can be a fixed file, or can be a new file supplied daily.
    Airflow context variables are supported for the file naming, e.g.
        TABLE_METADATA_FILE_{{ ds }}.csv
    for a metadata file supplied daily.

    The format of the metadata file should be a csv with one column as follows:
        FILE_NAME_1
        ...
        FILE_NAME_N
    with all files to ingest
    """
    source_type = "GCS"

    def flag_file_sensor(self, table_config, taskgroup):
        if "flag_file_path" in table_config.extra_options.get("file_table_config"):
            flag_file_path = table_config.extra_options.get("file_table_config")["flag_file_path"]
            bucket = self.config.source.extra_options["gcs_bucket"]
            return GCSObjectExistenceSensor(
                task_id="wait_for_flag_file",
                bucket=bucket,
                object=flag_file_path,
                task_group=taskgroup
            )
        else:
            return None

    def file_ingestion_task(self, table_config, taskgroup):
        """
        No ingestion is needed - data is already in GCS, so return a dummy operator.
        """
        return None

    def file_sensor(self, table_config, taskgroup):
        """
        Returns an Airflow sensor that waits for the list of files specified by the metadata file provided.
        """
        bucket = self.config.source.extra_options["gcs_bucket"]
        table_name = table_config.table_name
        files_to_wait_for = "{{ ti.xcom_pull(key='file_list', task_ids='" + table_name + ".ftp_taskgroup.get_file_list') }}"

        if self.config.source.extra_options["file_source_config"]["file_prefix_filtering"]:
            return GCSObjectPrefixListExistenceSensor(
                task_id="wait_for_files_to_ingest",
                bucket=bucket,
                prefixes=files_to_wait_for,
                task_group=taskgroup
            )
        else:
            return GCSObjectListExistenceSensor(
                task_id="wait_for_files_to_ingest",
                bucket=bucket,
                objects=files_to_wait_for,
                task_group=taskgroup
            )

    def load_to_landing(self, table_config, **kwargs):
        gcs_hook = GCSHook()
        file_source_config = from_dict(data_class=FileSourceConfig, data=self.config.source.extra_options["file_source_config"])

        # Parameters
        ds = kwargs['ds']
        ti = kwargs['ti']

        data_source = self.config.source
        bucket = data_source.extra_options["gcs_bucket"]
        source_format = file_source_config.source_format
        field_delimeter = file_source_config.delimeter
        gcp_project = data_source.gcp_project
        landing_dataset = data_source.landing_zone_options.landing_zone_dataset
        landing_table_name = table_config.landing_zone_table_name_override
        table_name = table_config.table_name
        destination_table = f"{gcp_project}:{landing_dataset}.{table_config.landing_zone_table_name_override}" + f"_{ds}"

        if "skip_gcs_upload" not in data_source.extra_options["file_source_config"]:
            files_to_load = ti.xcom_pull(key='file_list', task_ids=f'{table_name}.ftp_taskgroup.get_file_list')
        else:
            dir_prefix = table_config.extra_options.get("file_table_config")["directory_prefix"]
            dir_prefix = dir_prefix.replace("{{ ds }}", ds)
            files_to_load = [dir_prefix]

        gcs_bucket_prefix = file_source_config.gcs_bucket_prefix
        if gcs_bucket_prefix is None:
            gcs_bucket_prefix = ""
        if not gcs_bucket_prefix == "":
            gcs_bucket_prefix += "/"

        destination_path_prefix = gcs_bucket_prefix 
        if "gcs_bucket_path_format_mode" in self.config.source.extra_options["file_source_config"]:
            date = datetime.strptime(ds, '%Y-%m-%d').strftime('%Y/%m/%d')
            destination_path_prefix = gcs_bucket_prefix + table_name + "/" + date
            logging.info(destination_path_prefix)

            files_to_load = [destination_path_prefix + "/" + f for f in files_to_load]
            logging.info(files_to_load)

        if "parquet_upload_option" in table_config.extra_options.get("file_table_config"):
            parquet_upload_option = table_config.extra_options.get("file_table_config")["parquet_upload_option"]
        else:
            parquet_upload_option = "BASH"

        source_format = file_source_config.source_format
        if source_format == "PARQUET" and parquet_upload_option == "BASH":
            date_column = table_config.extra_options.get("sftp_table_config")["date_column"]
            gcs_bucket_prefix = file_source_config.gcs_bucket_prefix
            # bq load command if parquet
            partition_prefix = ti.xcom_pull(key='partition_prefix', task_ids=f'{table_name}.ftp_taskgroup.load_sftp_to_gcs')
            if not partition_prefix:
                partition_prefix = self.config.source.extra_options["sftp_source_config"]["partition_prefix"]
                partition_prefix = partition_prefix.replace("date", table_config.extra_options.get("sftp_table_config")["date_column"])
                partition_prefix = partition_prefix.replace("ds", kwargs['prev_ds'])
            if "prefix" in table_config.extra_options.get("file_table_config"):
                partition_prefix = partition_prefix + "/" + table_config.extra_options.get("file_table_config")["prefix"]
            command = self.get_load_script(gcp_project, landing_dataset, landing_table_name + f"_{ds}", bucket, gcs_bucket_prefix, partition_prefix, table_name, date_column, ds)
            logging.info(command)
            try:
                bash = BashOperator(
                    task_id="import_files_to_bq_landing",
                    bash_command=command
                )
                bash.execute(context=kwargs)
            except Exception:
                logging.info("Load into BQ landing zone failed.")
        else:
            # gcs->bq operator else
            if file_source_config.file_prefix_filtering:
                for i in range(len(files_to_load)):
                    matching_gcs_files = gcs_hook.list(bucket_name=bucket, prefix=files_to_load[i])
                    logging.info(matching_gcs_files)
                    if len(matching_gcs_files) > 1:
                        raise AirflowException(f"There is more than one matching file with the prefix {files_to_load[i]} in the bucket {bucket}")
                    files_to_load[i] = matching_gcs_files[0]
            else:
                files_to_load = [f"{gcs_bucket_prefix}{table_name}/{ds}/" + f for f in files_to_load]

            schema_file_name = None
            if "schema_file" in table_config.extra_options.get("file_table_config"):
                schema_file_name = table_config.extra_options.get("file_table_config")["schema_file"]

            allow_quoted_newlines = False
            if "allow_quoted_newlines" in table_config.extra_options.get("file_table_config"):
                allow_quoted_newlines = table_config.extra_options.get("file_table_config")["allow_quoted_newlines"]

            if parquet_upload_option == "GCS" and source_format == "PARQUET":
                prefix = ""
                if "prefix" in table_config.extra_options.get("file_table_config"):
                    prefix = table_config.extra_options.get("file_table_config")["prefix"]
                prefix = destination_path_prefix + "/" + prefix
                # logging.info(destination_path_prefix + "/" + partition_prefix)
                files_to_load = gcs_hook.list(bucket_name=bucket, prefix=prefix)

            # Get files to load from metadata file
            if schema_file_name:
                schema_file = gcs_hook.download(bucket_name=bucket, object_name=schema_file_name)
                # Only supports json schema file format - add additional support if required
                schema_fields = json.loads(schema_file)
                gcs_to_bq = GCSToBigQueryOperator(
                    task_id='import_files_to_bq_landing',
                    bucket=bucket,
                    source_objects=files_to_load,
                    source_format=source_format,
                    schema_fields=schema_fields,
                    field_delimiter=field_delimeter,
                    destination_project_dataset_table=destination_table,
                    allow_quoted_newlines=allow_quoted_newlines,
                    write_disposition='WRITE_TRUNCATE',
                    create_disposition='CREATE_IF_NEEDED',
                    skip_leading_rows=1,
                )
            else:
                gcs_to_bq = GCSToBigQueryOperator(
                    task_id='import_files_to_bq_landing',
                    bucket=bucket,
                    source_objects=files_to_load,
                    source_format=source_format,
                    field_delimiter=field_delimeter,
                    destination_project_dataset_table=destination_table,
                    allow_quoted_newlines=allow_quoted_newlines,
                    write_disposition='WRITE_TRUNCATE',
                    create_disposition='CREATE_IF_NEEDED',
                    skip_leading_rows=1,
                )
            gcs_to_bq.execute(context=kwargs)

            kwargs['ti'].xcom_push(key='loaded_files', value=files_to_load)

    def delete_files(self, table_config, **kwargs):
        ti = kwargs["ti"]
        table_name = table_config.table_name
        files_to_load = ti.xcom_pull(key='loaded_files', task_ids=f'{table_name}.ftp_taskgroup.load_gcs_to_landing_zone')
        data_source = self.config.source
        bucket = data_source.extra_options["gcs_bucket"]
        gcs_hook = GCSHook()

        for file in files_to_load:
            gcs_hook.delete(bucket_name=bucket, object_name=file)

    def delete_gcs_files(self, table_config, taskgroup):
        return PythonOperator(
            task_id="delete_gcs_files",
            op_kwargs={"table_config": table_config},
            python_callable=self.delete_files,
            task_group=taskgroup
        )

    def validate_extra_options(self):
        # GCS Source only requires the checks for the base file_source_config and file_table_configs:
        # other sources like SFTP require extra checks
        super().validate_extra_options()
