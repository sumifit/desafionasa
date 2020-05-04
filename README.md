![Desafio Nasa](https://vdmedia.elpais.com/elpaistop/201810/27/2018102792523258_1540625246_video_1540625166.jpg)
# ***Desafio Nasa***

> Esse desafio utilizei DOCKER e CLUSTER SPARK com 3 nodes

Abaixo consta as perguntas que foram feita no arquivo ![](https://github.com/sumifit/desafionasa/blob/master/Desafio_NASA.pdf)

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



```

g1) Número de hosts únicos?

![Host Unicos](https://github.com/sumifit/desafionasa/blob/master/1-Hostunicos.PNG)

g2) Total de erros 404

![Total erro 404](https://github.com/sumifit/desafionasa/blob/master/2-total_erros_404.PNG)

g3) Os 5 URLs que mais causaram erro 404

![5 URL mais erro 404](https://github.com/sumifit/desafionasa/blob/master/3-As5URLs_mais_erro_404.PNG)

g4) Quantidade de erros 404 por dia

![Quantidade erro 404 por dia](https://github.com/sumifit/desafionasa/blob/master/4-QuantidadeErros404PorDia.PNG)

> Não consegui usar o ```dayofmonth ``` do pyspark para pegar somente o dia, infelizmente! :(

g5) O total de bytes retornados

![Total bytes](https://github.com/sumifit/desafionasa/blob/master/5-Total_bytes_retornados.PNG)
