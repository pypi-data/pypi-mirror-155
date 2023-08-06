import re
import sys
from pyspark.sql import types

def make_spark_schema(raw):
    if not isinstance(raw, str):
        print('USAGE: make_spark_schema(sting)')
        print('Example: make_spark_schema(str(spark.sql.DataFram(<Pandas DataFrame>).schema))')
        sys.exit(1)

    fields = []
    
    for i in zip([i.start() for i in re.finditer("\(",raw)][2:],[i.start() for i in re.finditer("\)",raw)][:-2]):
        fields.append(raw[i[0]+1:i[1]])

    schema = "types.StructType[\n"

    ending = '\n'
    commas = len(fields) -1
    
    for f in fields:
        n = f.split(",")
        schema = schema+"\ttypes.StructField(\""+n[0]+"\", types."+n[1]+"(), "+n[2].capitalize()+")"
        if commas > 0:
            schema = schema + ',' + ending
            commas -= 1
    schema = schema + ending
    schema = schema +"])"
    print(schema)

def make_delta_schema(file, table_name='your_table', db = 'default', delta_loc='./delta'):
    print("spark.sql('''")
    print(f"CREATE TABLE IF NOT EXISTS {db}.{table_name}")
    holder = str(spark.read.parquet(file).schema)
    fields = holder.split('(')
    for i in fields:
        if ',' in i:
            col = i.split(',')[0:2]
            print('\t'+col[0]+','+col[1])
    print("    ) USING DELTA\n\tLOCATION \"{0}\""+f"\n\t'''.format('{delta_loc}')")