# Summary
<br>
Sometimes when converting a Pandas DataFrame to a Spark DataFrame variables are not interpreted correctly<br> 
which can lead a programmer to have to type many lines of code and then provide the schema when building the<br>
Spark DataFrame.
<br><br>
Additionally this is true for defining a Delta Table before loading your parquet files. This package contains<br>
two functions aimed at creating these definitions which will hopefully cut down on a lot of typing and speed <br>
up development time for the user. <br><br>

## Installation
pip install SparkSchemafy
<br><br>
## Usage
from schemafy import make_spark_schema, make_delta_schema
<br><br>
### Make a Spark DataFrame Schema from a Pandas DataFrame<br>
make_spark_schema(str(spark.sql.DataFram(<Pandas DataFrame>).schema))
<br><br>
### Make a delta table schema from parquet file<br>
make_delta_schema('<your file>.parquet')