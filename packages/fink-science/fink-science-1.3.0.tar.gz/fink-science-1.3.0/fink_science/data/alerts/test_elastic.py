import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from fink_science.utilities import concat_col

from fink_science.utilities import concat_col
from fink_science.random_forest_snia.processor import rfscore_sigmoid_elasticc
from fink_science.snn.processor import snn_ia_elasticc

import numpy as np

@F.pandas_udf(IntegerType(), F.PandasUDFType.SCALAR)
def cf(filtercode):
    return filtercode.apply(lambda array: np.sum([x in ['g', 'r'] for x in array]))

spark = SparkSession.Builder().getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = spark.read.format('avro')\
    .load('/Users/julien/Documents/workspace/myrepos/fink-science/fink_science/data/alerts/elasticc')

what = ['midPointTai', 'filterName', 'psFlux', 'psFluxErr']
prefix = 'c'
what_prefix = [prefix + i for i in what]

for colname in what:
    df = concat_col(
        df, colname, prefix=prefix,
        current='diaSource', history='prvDiaSources'
    )

df = df.withColumn('deltat', F.array_max('cmidPointTai') - F.array_min('cmidPointTai'))
df = df.withColumn('len', cf('cfilterName'))
df = df.withColumn('cdsxmatch', F.lit('Unknown'))
df = df.withColumn('roid', F.lit(0))

# AL
args = [F.col(i) for i in what_prefix]
args += [F.col('cdsxmatch'), F.col('diaSource.nobs')]
df = df.withColumn('pIa', rfscore_sigmoid_elasticc(*args))


# SNN
# args = [F.col('diaSource.diaSourceId')]
# args += [F.col(i) for i in what_prefix]
# args += [F.col('roid'), F.col('cdsxmatch'), F.array_min('cmidPointTai')]
# args += [F.lit('snn_snia_vs_nonia')]
# df = df.withColumn('pIa', snn_ia_elasticc(*args))

# missing_one_band = df.filter(df['pIa'] == 0.0).count()
#
# flagged_out = df.filter(df['pIa'] == -1.0).count()
#
# print(df.count(), missing_one_band, flagged_out)
#
df.filter(df['pIa'] > 0.0).select(['pIa', 'diaSource.nobs', 'len', 'deltat']).summary().show()

# df.filter(df['pIa'] > 0.2).select(['pIa', 'diaSource.diaSourceId', 'diaSource.nobs', 'len', 'deltat']).orderBy('pIa', ascending=False).show()

# df.filter(df['len'] == 2).select(['pIa', 'diaSource.diaSourceId', 'diaSource.nobs', 'len']).orderBy('pIa', ascending=False).show()
# df.filter(df['len'] == 15).select(['pIa', 'diaSource.diaSourceId', 'diaSource.nobs', 'len']).orderBy('pIa', ascending=False).show()
# df.select(['pIa', 'diaSource.diaSourceId', 'diaSource.nobs', 'len']).orderBy('pIa', ascending=False).show()

# df.filter(df['pIa'] > 0.2).repartition(4).write.parquet('elasticc_parquet')
