from pyspark.sql import SparkSession
from pyspark.sql.functions import sum
from pyspark.sql.functions import col
import unidecode

# Create a SparkSession
spark = SparkSession.builder.appName("Read from HDFS").getOrCreate()

# # Read a file from HDFS
df = spark.read.csv("hdfs://namenode:9000/danh_sach_sv_de.csv")
df = df.select(
    col("_c0").alias("student_code"),
    col("_c1").alias("student_name"),
)

# Read parquet
parquet = spark.read.parquet("hdfs://namenode:9000/raw_zone/fact/activity/")
res = (
    parquet.groupBy("student_code", "activity", "timestamp")
    .agg(sum("numberOfFile").alias("totalFiles"))
    .orderBy("timestamp")
)

# Join
final = df.join(res, "student_code", "left").select(
    col("timestamp"), col("student_code"), col("student_name"), col("totalFiles")
)
student_code = df.select("student_code").distinct().rdd.flatMap(lambda x: x).collect()
student_name = df.select("student_name").distinct().rdd.flatMap(lambda x: x).collect()

for i, id in enumerate(student_code):
    student_df = final.filter(col("student_code") == id).orderBy("timestamp")
    student_name[i] = unidecode.unidecode(student_name[i])
    name = "_".join(student_name[i].split(" "))

    student_df.toPandas().to_csv(
        f""
    )  # .write.csv(f"hdfs://namenode:9000/res/{id}_{name}.csv", header=True)

final.show(20)
spark.stop()
