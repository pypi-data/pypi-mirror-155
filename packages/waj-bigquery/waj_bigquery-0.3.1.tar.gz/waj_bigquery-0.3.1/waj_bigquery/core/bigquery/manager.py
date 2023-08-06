import json
import os

from google.cloud import bigquery as bq
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account


def build_schema_sintax(table_columns) -> list:
    """
    Build schema sintax

    Description:
        - This utils function allows to create an specific python sintax to build a table in BigQuery

    Parameters:
        - table_columns: list of dict with table columns description

    Returns:
        - Returns a table_schema list with bigquery columns objects
    """
    table_schema = []
    for col in table_columns:
        # If table has relations this should be the proccess for nested fields
        if "fields-relationed" in col:
            fields = [
                bq.SchemaField(
                    name=f["field-name"],
                    field_type=f["field-type"],
                    mode=f["field-mode"],
                )
                for f in col["fields-relationed"]
            ]

            table_schema.append(
                bq.SchemaField(
                    name=col["column-name"],
                    field_type=col["column-type"],
                    mode=col["column-mode"],
                    description=col["column-description"],
                    fields=fields,
                )
            )
        else:
            table_schema.append(
                bq.SchemaField(
                    name=col["column-name"],
                    field_type=col["column-type"],
                    mode=col["column-mode"],
                    description=col["column-description"],
                )
            )

    return table_schema


class BigQueryManager:
    """
    This class allows you to manage models and upload information to Bigquery
    """

    def __init__(self, bigquery_client):
        self.client = bigquery_client
        self.BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")

    def create_or_get_dataset(self, dataset_id, location) -> bq.dataset.Dataset:
        """
        Description
        -----------------------
            This function look for an specific BigQuery dataset, if not found try to create otherwise return dataset

        Arguments
        -----------------------
            dataset_id str:
                name of desired dataset

            location: str
                place to host the dataset, Google code for location

        Returns
        -----------------------
            Returns a Bigquery dataset created on top of the google platform
        """
        try:
            dataset = self.client.get_dataset(dataset_id)
            return dataset
        except NotFound:
            dataset = bq.Dataset(dataset_id)
            dataset.location = location
            dataset = self.client.create_dataset(dataset, timeout=30)
            return dataset

    def check_if_table_exist(self, table_id) -> bool:
        """
        Description
        -----------------------
            This function check if table exists in Bigquery

        Arguments
        -----------------------
            table_id: str
                name of table

        Returns
        -----------------------
            Bool, true if table exists or false if not
        """
        try:
            self.client.get_table(table_id)
            return True
        except NotFound:
            return False

    def get_actual_table_schema(self, table_id):
        """
        Description
        -----------------------
            This function returns the current schema for a given table

        Arguments
        -----------------------
            table_id: str
                Id for table id in bigquery

        Returns
        -----------------------
            This class return a schema for an specific Bigquery table_id
        """
        try:
            table = self.client.get_table(table_id)
            actual_schema = table.schema
            return actual_schema
        except NotFound:
            return None

    def create_or_update_model(self, model) -> list:
        """
        Description:
        -----------------------
            This function finds a json file called model_name and finds whether
            or not it is already in Bigquery, then it tries to create all
            the schema and model for the tables that are not there, or columns
            that are not there.

        Arguments
        -----------------------
            model: json_str
                This is the specific model that is required to build the database tables

        Returns
        -----------------------
            Returns list of dict message with the output of the each task
        """

        # 1. Set variable
        model = json.loads(model)

        output_result = []

        # with the model variable try to create or get a BigQuery dataset
        dataset_id = "{project_id}.{dataset_name}".format(
            project_id=self.BIGQUERY_PROJECT_ID, dataset_name=model["dataset_name"]
        )

        dataset = self.create_or_get_dataset(
            dataset_id=dataset_id, location=model["dataset_location"]
        )

        # iterate over tables in the model
        for table in model["tables"]:

            # Name of desired table in bigquery
            tbl_name = "{dataset_id}.{table_name}".format(
                table_name=table["table_name"], dataset_id=dataset_id
            )

            # Check if table id exists if not exists then create
            if self.check_if_table_exist(tbl_name):
                print(
                    "Table {} already exists in the dataset: {}".format(
                        table["table_name"], dataset_id
                    )
                )

                # If table already exists validate if the new schema has a new column to add
                # Get actual table schema
                actual_schema = self.get_actual_table_schema(tbl_name)
                original_schema = actual_schema[:]

                # Get actual columns name
                actual_columns = [x.name for x in actual_schema]

                # Get map dataset from model from json
                total_schema = build_schema_sintax(table["columns"])
                new_columns = []

                for field in total_schema:  # Iterate over map json model daset
                    if (
                        field.name in actual_columns
                    ):  # If a new column appears that is not in the current schema then add it to the list of new columns
                        pass
                    else:
                        new_columns.append(field)

                # Add new columns to actual schema
                if not new_columns:
                    output_result.append(
                        {
                            "action": "Updating table",
                            "details": "The table {} already exists and there is no new columns to add".format(
                                tbl_name
                            ),
                        }
                    )
                else:
                    for col in new_columns:
                        # Add the new columns to the current BigQuery schema listing
                        actual_schema.append(col)

                    table = self.client.get_table(tbl_name)
                    table.schema = actual_schema
                    table = self.client.update_table(table, ["schema"])

                    # Validate if new columns were added
                    if (
                        len(table.schema)
                        == len(original_schema) + len(new_columns)
                        == len(actual_schema)
                    ):
                        output_result.append(
                            {
                                "action": "Add new column in the table {}".format(
                                    tbl_name
                                ),
                                "details": "A new column has been added. Total={}".format(
                                    len(new_columns)
                                ),
                            }
                        )
                    else:
                        output_result.append(
                            {
                                "action": "Add new column in the table {}".format(
                                    tbl_name
                                ),
                                "details": "The columns has not been added. Total={}".format(
                                    len(new_columns)
                                ),
                            }
                        )
            else:
                # Create the new table
                tbl = bq.Table(
                    dataset.table(table["table_name"]),
                    schema=build_schema_sintax(table["columns"]),
                )

                # Check if table is partitioned
                if table["is_partitioned"]:
                    tbl.time_partitioning = bq.TimePartitioning(
                        type_=bq.TimePartitioningType.DAY,
                        field=table[
                            "field-partition"
                        ],  # name of column to use for partitioning
                        require_partition_filter=True,
                        expiration_ms=None,
                    )
                table = self.client.create_table(tbl)
                output_result.append(
                    {"action": "Create table {}".format(tbl_name), "details": "OK"}
                )

        return output_result

    def upload_df_to_bqtable(
        self, df, dataset_id, table_id, chunk_size=10000, inferModel=False, schema=None
    ) -> dict:
        """
        Description
        -----------------------
            This class allows you to load all the information
            from a dataframe into an existing bigquery table.

        Arguments
        -----------------------
            df: pd.Dataframe
                DataFrame to load in bigquery

            chunksize: int, optional
                Number of rows to be inserted in each chunk from the dataframe.
                Set to None to load the whole dataframe at once.

            dataset_id: str
                Specific dataset name in bigquery

            table_id: str
                Specific table name in bigquery

            inferModel: bool
                Check to decide if you want that model inferred from pandasDataFrame

            schema: list of dicts, optional
                List of BigQuery table fields to which according DataFrame columns conform to, e.g. [{'name': 'col1', 'type': 'STRING'},...]. If schema is not provided, it will be generated according to dtypes of DataFrame columns.
                See BigQuery API documentation on available names of a field.

        Returns
        -----------------------
            This function return a dictionary with result
        """

        try:
            df.to_gbq(
                destination_table="{}.{}".format(dataset_id, table_id),
                project_id=self.BIGQUERY_PROJECT_ID,
                if_exists="append",
                chunksize=chunk_size,
                table_schema=schema,
            )

            message = {
                "upload_data": True,
                "message": "All dataframe was loaded into bigquery",
            }

            return message

        except Exception as err:
            message = {"upload_data": False, "message": str(err)}
            return message
