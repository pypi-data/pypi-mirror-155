from pyspark.sql import DataFrame
from pyspark.sql.functions import (col, lit)
from pyspark.sql.types import StructType

def complete_dataframe(df: DataFrame, schema: StructType) -> DataFrame:
    for field in schema.fields:
        if field.name not in df.schema.fieldNames():
            df = df.withColumn(field.name, lit(None).cast(field.dataType))
    return df

def cast_dataframe(df: DataFrame, schema: StructType) -> DataFrame:
    for field in schema.fields:
        df = df.withColumn(field.name, col(field.name).cast(field.dataType))
    return df

def select_schema_columns(df: DataFrame, schema: StructType) -> DataFrame:
    return df.select(
        *[field.name for field in schema.fields]
    )