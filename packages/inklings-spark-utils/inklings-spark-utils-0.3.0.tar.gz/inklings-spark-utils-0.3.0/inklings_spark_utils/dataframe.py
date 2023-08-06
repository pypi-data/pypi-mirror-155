from pyspark.sql import DataFrame
from pyspark.sql.functions import (col, lit)
from pyspark.sql.types import StructType

def complete_dataframe(df: DataFrame, schema: StructType) -> DataFrame:
    current_fields = [field.name for field in df.schema.fields]
    expected_fields = { field.name:field.dataType for field in schema.fields}

    fields_to_add = expected_fields.keys() - set(current_fields)
     
    return df\
        .select(
           *[col(f) for f in current_fields],
           *[lit(None).cast(expected_fields[f]).alias(f) for f in fields_to_add] 
        )

def cast_dataframe(df: DataFrame, schema: StructType) -> DataFrame:
    current_fields = [field.name for field in df.schema.fields]
    expected_fields = { field.name:field.dataType for field in schema.fields}

    current_fields_not_casteable = set(current_fields) - expected_fields.keys()
    fields_to_cast = set(expected_fields.keys()).intersection(set(current_fields))
     
    return df\
        .select(
           *[col(f) for f in current_fields_not_casteable],
           *[col(f).cast(expected_fields[f]).alias(f) for f in fields_to_cast] 
        )

def select_schema_columns(df: DataFrame, schema: StructType) -> DataFrame:
    return df.select(
        *[field.name for field in schema.fields]
    )