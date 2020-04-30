![Desafio Nasa](https://vdmedia.elpais.com/elpaistop/201810/27/2018102792523258_1540625246_video_1540625166.jpg)
# ***Desafio Nasa***

Abaixo consta as perguntas que foram feita no arquivo PDF

a) Qual é o objetivo do comando ***cache*** em ***Spark***?

b) O mesmo código implementado em ***Spark*** é normalmente mais rápido que a implementação equivalente em MapReduce. Por quê?

c) Qual é a função do ***SparkContext***?

d) Explique com suas palavras o que é ***Resilient Distributed Datasets*** (RDD).

e) ***GroupByKey*** é menos eficiente que ***reduceByKey*** em grandes dataset. Por quê?

f) Explique o que o código ***Scala*** abaixo faz:

```scala
val textFile = sc.textFile("hdfs://...")
val counts = textFile.flatMap(line => line.split(" "))
          .map(word => (word, 1))
          .reduceByKey(_ + _)
counts.saveAsTextFile("hdfs://...")
```

g) Código elaborado em uma linguagem (***Python*** ou ***Scala***) utilizando ***Spark*** e responder as questões abaixo:

>Baseando-se em 02 arquivos da NASA, o proposto abaixo é para se desenvolver um código em minha linguagem de preferência.

>Fonte oficial do dateset: http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html
Dados:

>Jul 01 to Jul 31, ASCII format, 20.7 MB gzip compressed, 205.2 MB.

>Aug 04 to Aug 31, ASCII format, 21.8 MB gzip compressed, 167.8 MB.

Levando em consideração que o DATASET está em formato ASCII com as seguintes colunas

CAMPO|TIPO|DESCRIÇÃO
---|---|---
HOSTNAME|STRING|ENDEREÇO IP OU URL
TIMESTAMP|DATE| DATA E HORA EM TIMEZONE
REQUISICAO|STRING| CODIGO COMPLETA DA REQUISIÇÃO
HTTP_CODE|NUMBER| CODIGO DE RESPOSTA HTTP ([Para saber mais])(https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
TOTAL_BYTES|NUMBER|TOTAL DE BYTES

>Abaixo consta o codigo python utilizado

```python
import pyspark
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import re
from pyspark.sql.functions import UserDefinedFunction

spark = SparkSession.builder.appName('Nasa').getOrCreate()

# Gera estrura dataframe
df_jul95_struture = [StructField("HOSTNAME",StringType(), True),\
            StructField("TIMESTAMP", StringType(), True),\
            StructField("REQUISICAO", StringType(), True),\
            StructField("HTTP_CODE", StringType(), True),\
            StructField("TOTAL_BYTES", StringType(), True)]
jul_95schema = StructType(df_jul95_struture)
df_jul95_s = spark.createDataFrame([],jul_95schema)

#df_jul95_s.show()

# Gera dataframe from FILE ASCII
df_jul95 = spark.read.csv("/spark/nasafiles/NASA_access_log_Jul95")

# Replace dataframe caracter - passo 1
udf = UserDefinedFunction(lambda x: re.sub(' - - ','|',x), StringType())
new_df = df_jul95.select(*[udf(column).alias(column) for column in df_jul95.columns])
new_df.collect()
new_df.write.csv('/home/nasa_jul95.txt')
new_df.show()

#df.repartition(1).write.format(new_df).save("nasa_jul95.csv",header = 'false')
# Replace datafram - passo2
#df_jul95_p1 = 
```

g1) Número de hosts únicos?

g2) Total de erros 404

g3) Os 5 URLs que mais causaram erro 404

g4) Quantidade de erros 404 por dia

g5) O total de bytes retornados
