import importlib

from johnsnowlabs.utils.enums import *


def is_spark_version_env(spark_version: str) -> bool:
    import pyspark
    env_spark_version = pyspark.__version__[0:-2].replace(".", "")
    return spark_version in env_spark_version


def try_import_lib(lib: str, print_failure=False):
    try:
        importlib.import_module(lib)
        return True
    except Exception as err:
        if print_failure:
            print(f'Failed to import {lib}. Seems not installed.')


class JslLibDependencyResolverABC(ABC):
    has_gpu_jars: bool
    has_cpu_jars: bool
    product_name: ProductName



    @classmethod
    @abstractmethod
    def get_cpu_jar_urls(cls, jsl_lib_version: Optional[LibVersionIdentifier],
                         spark_version: Optional[JslLibSparkVersionIdentifier],
                         secret: Optional[str]) -> UrlDependency:
        raise Exception(f'{cls.product_name.value} has no CPU Jars!')

    @classmethod
    @abstractmethod
    def get_gpu_jar_urls(cls, jsl_lib_version: Optional[LibVersionIdentifier],
                         spark_version: Optional[JslLibSparkVersionIdentifier],
                         secret: Optional[str]) -> UrlDependency:
        raise Exception(f'{cls.product_name.value} has no GPU Jars!')

    @classmethod
    @abstractmethod
    def get_py_urls(cls, jsl_lib_version: LibVersionIdentifier,
                    spark_version: JslLibSparkVersionIdentifier,
                    secret: Optional[str], install_type: PyInstallTypes) -> UrlDependency:
        raise Exception(f'{cls.product_name.value} has no Py Dependencies!')

    @classmethod
    @abstractmethod
    def get_spark_version_id(cls, spark_version: Optional[str]) -> LibVersionIdentifier:
        """
        Get spark version representation within a specific JSL version which should be usable to build URL of dependencies
        This is used to locate remote dependencies, since every JSL-Lib refers to each Spark version in its own terminology
        I.e. spark_version==3.2.1 could be referred to as 3.2 in OCR and 3.2.1 in Spark NLP and 3 in Healthcare, etc.
        :param spark_version:
        :return:
        """
        pass

    @classmethod
    def get_version_from_lib_secret(cls, secret: str) -> LibVersionIdentifier:
        """
        Should call get_jsl_lib_version_identifier_for_spark_version
        :return: LibVersionIdentifier for the specific Resolver
        """
        return LibVersionIdentifier(secret.split('-')[0])

    @classmethod
    def get_installed_pyspark_version_or_latest_compatible(cls, ) -> LibVersionIdentifier:
        """
        Assumes Pyspark Installed.
        Import Pyspark, check version and get correct identifier based on that.
        Should call get_jsl_lib_version_identifier_for_spark_version
        :return: LibVersionIdentifier for the specific Resolver
        """
        pass
        """Get Pyspark version from installed pyspark or use latest pyspark if none installed"""
        # Infer spark version from Pyspark installed in current environment
        if try_import_lib('pyspark'):
            import pyspark
            spark_version = pyspark.__version__[0:-2].replace(".", "")
        else:
            spark_version = LatestCompatibleProductVersion.pyspark.value[0:-2].replace(".", "")
        return LibVersionIdentifier(spark_version)


