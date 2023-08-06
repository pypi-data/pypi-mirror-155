from pyspark.sql import *


class ProphecyDataFrame:
    def __init__(self, df: DataFrame, spark: SparkSession):
        self.jvm = spark.sparkContext._jvm
        self.sqlContext = SQLContext(spark.sparkContext, sparkSession=spark, jsqlContext=spark._jwrapped)
        if type(df) == DataFrame:
            self.extended_dataframe = self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
            self.dataframe = df
        else:
            self.extended_dataframe = self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
            self.dataframe = DataFrame(df, self.sqlContext)

    def interim(self, subgraph, component, port, subPath, numRows, interimOutput, detailedStats=False) -> DataFrame:
        result = self.extended_dataframe.interim(subgraph, component, port, subPath, numRows, interimOutput,
                                                 detailedStats)
        return DataFrame(result, self.sqlContext)

    def __getattr__(self, item: str):
        if item == "interim":
            self.interim

        if hasattr(self.extended_dataframe, item):
            return getattr(self.extended_dataframe, item)
        else:
            return getattr(self.dataframe, item)


class InterimConfig:

    def __init__(self, spark: SparkSession, sessionForInteractive: str = ""):
        self.interimOutput = spark.sparkContext._jvm.org.apache.spark.sql.InterimOutputHive2.apply(
            sessionForInteractive)


interimConfig = None


class MetricsCollector:
    @classmethod
    def initializeMetrics(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.initializeMetrics(spark._jsparkSession)

    @classmethod
    def start(cls, spark: SparkSession, sessionForInteractive: str = ""):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(spark._jsparkSession, sessionForInteractive)
        global interimConfig
        if interimConfig is None:
            interimConfig = InterimConfig(spark, sessionForInteractive)

    @classmethod
    def end(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.end()
        global interimConfig
        interimConfig = None


def collectMetrics(spark: SparkSession, df: DataFrame, subgraph: str, component: str, port: str,
                   numRows: int = 40) -> DataFrame:
    global interimConfig
    if interimConfig is None:
        interimConfig = InterimConfig(spark)
    pdf = ProphecyDataFrame(df, spark)
    return pdf.interim(subgraph, component, port, "dummy", numRows, interimConfig.interimOutput)
