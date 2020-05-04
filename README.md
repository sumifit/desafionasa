![Desafio Nasa](https://vdmedia.elpais.com/elpaistop/201810/27/2018102792523258_1540625246_video_1540625166.jpg)
# ***Desafio Nasa***

Abaixo consta as perguntas que foram feita no arquivo PDF

a) Qual é o objetivo do comando ***cache*** em ***Spark***?

>R: Utiliza-se cache no ***Spark*** para efetuar análise sem precisar transformar novamente o arquivo original em cada leitura. Essa transformação cria um ***Spark RDD*** resultante bem menor que o o arquivo original facilitando assim as manipulações e ganhando velocidade

b) O mesmo código implementado em ***Spark*** é normalmente mais rápido que a implementação equivalente em MapReduce. Por quê?

> Spark processa o código em memóri, já o Mapreduce faz a leitura do código no cluster, processa e retorna o dado para o cluster. Isso o torna mais lento que o Spark

c) Qual é a função do ***SparkContext***?

> É o objeto que conecta o Spark ao programa que está sendo desenvolvido. Ele pode ser acessado como uma variável em um programa para utilizar os seus recursos.

d) Explique com suas palavras o que é ***Resilient Distributed Datasets*** (RDD).

>R: RDD é uma estrutura de dados utilizada pelo Spark que contém conjuntos de dados e que são divididos em partições lógicas. RDD tem como objetivo a manipulação de dados e é a representação de um dado distribuido nos nós do cluster e que pode ser processado em paralelo.

e) ***GroupByKey*** é menos eficiente que ***reduceByKey*** em grandes dataset. Por quê?

>GroupByKey tem uma desvantagem justamente por ele transferir todo o Dataset pela rede, enquanto o o reduceByKey calcula somas locais para cada chave em cada partição e combina essas somas locais em somas maiores.

f) Explique o que o código ***Scala*** abaixo faz:

```scala
val textFile = sc.textFile("hdfs://...")
val counts = textFile.flatMap(line => line.split(" "))
          .map(word => (word, 1))
          .reduceByKey(_ + _)
counts.saveAsTextFile("hdfs://...")
```

>R: Lê um determinado conteúdo em um diretório do HDFS, faz um split de coluna onde o delimitador é ESPAÇO, conta cada palavra, faz um group by com a função reduceByKey e depois salva o resultado em um novo dataset no HADOOP (HDFS).

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

![Host Unicos](https://github.com/sumifit/desafionasa/blob/master/1-Hostunicos.PNG)

g2) Total de erros 404

![Total erro 404](https://github.com/sumifit/desafionasa/blob/master/2-total_erros_404.PNG)

g3) Os 5 URLs que mais causaram erro 404

![5 URL mais erro 404](https://github.com/sumifit/desafionasa/blob/master/3-As5URLs_mais_erro_404.PNG)

g4) Quantidade de erros 404 por dia

TIPO|TOTAL
---|---
URL 404 POR DIA|0

g5) O total de bytes retornados

![Total bytes](https://github.com/sumifit/desafionasa/blob/master/5-Total_bytes_retornados.PNG)
