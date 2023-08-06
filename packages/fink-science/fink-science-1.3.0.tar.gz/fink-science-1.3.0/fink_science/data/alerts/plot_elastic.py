import matplotlib.pyplot as plt
import seaborn as sns

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from fink_science.utilities import concat_col

import numpy as np

sns.set_context('talk')

def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [
        (h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]
    ]
    ax.legend(*zip(*unique), framealpha=0.3)

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

# oids = [840057]
oid = 846028

cols = ['cmidPointTai', 'cfilterName', 'cpsFlux', 'cpsFluxErr', 'diaSource.nobs']
pdf = df.filter(df['diaSource.diaSourceId'] == oid).select(cols).toPandas()

print(len(pdf), pdf['nobs'], len(pdf['cmidPointTai'].values[0]))

fig, ax = plt.subplots(figsize=(12, 5))
fig.set_dpi(150)

colordic = {
    'u': 'C0',
    'g': 'C1',
    'r': 'C2',
    'i': 'C3',
    'z': 'C4',
    'Y': 'C5',
}

for i in range(len(pdf['cmidPointTai'].values[0])):
    plt.errorbar(
        pdf['cmidPointTai'].values[0][i],
        pdf['cpsFlux'].values[0][i],
        pdf['cpsFluxErr'].values[0][i],
        label=pdf['cfilterName'].values[0][i],
        color=colordic[pdf['cfilterName'].values[0][i]], ls='', marker='o'
    )
    if pdf['cfilterName'].values[0][i] in ['g', 'r']:
        plt.axvline(pdf['cmidPointTai'].values[0][i], ls='--', color='black', alpha=0.5)

plt.xlabel('MJD')
plt.ylabel('Flux')
plt.title('diaObjectId {}'.format(oid))
plt.tight_layout()
legend_without_duplicate_labels(ax)
# plt.savefig('1161.png')
plt.show()
