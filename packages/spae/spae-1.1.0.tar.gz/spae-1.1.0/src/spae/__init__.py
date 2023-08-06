from uuid import uuid4
from pyspark.sql import SparkSession

from .aql.compiler import Compiler
from .aggregation import DataBase


class Spae:
    '''
    spae Client for AQL Compilation
    '''

    def __init__(self, spark_url, additional_jars=[], additional_packages=[], lazy=False):
        self.spark_url = spark_url
        self.lazy = lazy
        self.spark = None
        self.additional_jars = additional_jars
        self.additional_packages = additional_packages
        self.db_configuration = {}
        if not lazy:
            self.build_session()

    def register_db(self, name=None, url=None, user=None, password=None, db_type='postgres'):
        if not name:
            name = 'default'

        self.db_configuration[name] = DataBase(self, name, url, user, password, db_type)

    def build_session(self):
        builder = SparkSession.builder.master(self.spark_url)
        if self.additional_jars:
            builder = builder.config("spark.jars", ','.join(self.additional_jars))

        if self.additional_packages:
	        builder = builder.config('spark.jars.packages', ','.join(self.additional_packages))

        self.spark = (
            builder
            .appName('SPAE')
            .getOrCreate()
        )

    def aggregate(self, aql):
        if self.spark is None:
            self.build_session()

        compiler = Compiler(self)
        compiler.pre_compile(aql)
        return compiler.run()