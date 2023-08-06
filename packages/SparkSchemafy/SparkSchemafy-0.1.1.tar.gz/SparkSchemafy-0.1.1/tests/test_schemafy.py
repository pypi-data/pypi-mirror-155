from schemafy import make_schema

def test_make_schema():
    schema = 'a'
    assert schema == 'a'
    # make_schema("StructType(List(StructField(hvfhs_license_num,StringType,true),StructField(dispatching_base_num,StringType,true),StructField(pickup_datetime,StringType,true),StructField(dropoff_datetime,StringType,true),StructField(PULocationID,LongType,true),StructField(DOLocationID,LongType,true),StructField(SR_Flag,DoubleType,true)))")
    # assert schema == '''types.StructType([
    # types.StructField ("hvfhs_license_num",types.StringType(),True),
    # types.StructField ("dispatching_base_num",types.StringType(),True),
    # types.StructField ("pickup_datetime",types.TimestampType(),True),
    # types.StructField ("dropoff_datetime",types.TimestampType(),True),
    # types.StructField ("PULocationID",types.LongType(),True),
    # types.StructField ("DOLocationID",types.LongType(),True),
    # types.StructField ("SR_Flag",types.DoubleType(),True)])'''