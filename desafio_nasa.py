import pyspark.sql.functions as f
from pyspark.sql.functions import year,month, dayofmonth
from functools import reduce
from pyspark.sql import SparkSession

# inicializando contexto spark
spark = SparkSession.builder.appName('Nasa').getOrCreate()

# lendo o primeiro arquivo 
df_jul95 = spark.read.text("/spark/nasafiles/NASA_access_log_Jul95")
# lendo o segundo arquivo
df_aug95 = spark.read.text("/spark/nasafiles/NASA_access_log_Aug95")
# efetuando UNION entre os arquivos e gerando um unico dataframe
result = df_jul95.union(df_aug95)

# dataframe por regex
split_df = result.select(f.regexp_extract('value', r'^([^\s]+\s)', 1).alias('host'),
                          f.regexp_extract('value', r'^.*\[(\d\d/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})]', 1).alias('timestamp'),
                          f.regexp_extract('value', r'^.*"\w+\s+([^\s]+)\s+HTTP.*"', 1).alias('path'),
                          f.regexp_extract('value', r'^.*"\s+([^\s]+)', 1).cast('integer').alias('status'),
                          f.regexp_extract('value', r'^.*\s+(\d+)$', 1).cast('integer').alias('content_size')
                          )

# 1)numero hosts unicos
dfhostsunicos=split_df.groupBy("host").count().orderBy('count', ascending=False).show(truncate=False)                        

# 2)total erros 404
df404total=split_df.groupBy("status").count().where("status = 404").show()

# 3) 5 urls que mais causaram erro 404
df404_top5=split_df.where("status = 404").groupBy('host').count().orderBy('count', ascending=False).show(n=5)

# 4) Quantidade de erros 404 por dia

split_df_distinct = split_df.select(split_df.host, split_df.timestamp).distinct().where("status = 404") # Cria um dataset de timestamp com distinct
df_erros_dia_404 = split_df_distinct.groupBy('timestamp').count()
df_erros_dia_404.orderBy('count', ascending=False).show()

# 5) Quantidade total de bytes retornados
dfbytes=split_df.groupBy("content_size").sum().show()


