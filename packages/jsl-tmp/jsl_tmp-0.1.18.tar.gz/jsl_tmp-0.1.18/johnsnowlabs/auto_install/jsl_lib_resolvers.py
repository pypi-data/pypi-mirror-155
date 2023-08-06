import re
from abc import ABCMeta
from typing import Optional

import requests

from johnsnowlabs import ProductName, try_import_lib, PyInstallTypes
from johnsnowlabs.abstract_base.lib_resolvers import JslLibDependencyResolverABC
from johnsnowlabs.utils.enums import LibVersionIdentifier, JslLibSparkVersionIdentifier, UrlDependency, \
    JavaInstallTypes, OcrSparkVersionId, HcSparkVersionId, LatestCompatibleProductVersion, NlpSparkVersionId


class OcrLibResolver(JslLibDependencyResolverABC, metaclass=ABCMeta):
    """
    Each JslLibDependencyResolver util must implement the following :
    - get_jar_urls(lib_version,spark_version,Optional[secret])->UrlDependency
    - get_mvn_coordinates(lib_version,spark_version,Optional[secret])->RepoDependency
    - get_python_urls(lib_version,spark_version,Optional[secret],install_type)->UrlDependency
    - get_pypi_identifier(lib_version,spark_version,Optional[secret],install_type)->RepoDependency
    - get_lib_version_i

    """
    has_gpu_jars = False
    product_name = ProductName.ocr

    @classmethod
    def get_jsl_lib_version(cls, secret: Optional[str] = None) -> LibVersionIdentifier:
        if not secret:
            try_import_lib('sparkocr', True)
            import sparkocr
            jsl_lib_version = sparkocr.version()
        else:
            jsl_lib_version = secret.split('-')[0]
        return LibVersionIdentifier(jsl_lib_version)

    @classmethod
    def get_cpu_jar_urls(cls, secret: Optional[str],
                         jsl_lib_version: Optional[LibVersionIdentifier] = None,
                         spark_version: Optional[JslLibSparkVersionIdentifier] = None, ) -> UrlDependency:
        """
        Applicable spark version = 23,30,32
        :return:
        """
        if not spark_version:
            spark_version = cls.get_spark_version_id()
        if not jsl_lib_version:
            jsl_lib_version = cls.get_version_from_lib_secret(secret)
        jar_loc = f'https://pypi.johnsnowlabs.com/{secret}/' \
                  f'jars/spark-ocr-assembly-{jsl_lib_version}-spark{spark_version}.jar'
        return UrlDependency(jar_loc, JavaInstallTypes.jar.value)

    @classmethod
    def get_py_urls(cls, secret: str, jsl_lib_version: Optional[LibVersionIdentifier] = None,
                    install_type: PyInstallTypes = PyInstallTypes.wheel,
                    spark_version: Optional[JslLibSparkVersionIdentifier] = None) -> UrlDependency:
        """
        install_type_tar = '.tar.gz'
        install_type_wheel = '-py3-none-any.whl'
        Applicable spark version = 23,30,32
        :return:
        """

        if not spark_version:
            spark_version = cls.get_spark_version_id()
        if not jsl_lib_version:
            jsl_lib_version = cls.get_version_from_lib_secret(secret)

        install_loc = f'https://pypi.johnsnowlabs.com/{secret}/' \
                      f'spark-ocr/spark-ocr-{jsl_lib_version}+spark{spark_version}{install_type.value}'
        if install_type == PyInstallTypes.wheel:
            # Wheels use a '_' instead of '-' in the url
            install_loc = install_loc.replace(f'spark-ocr/spark-ocr-', f'spark-ocr/spark_ocr-')
        return UrlDependency(install_loc, install_type.value)

    @classmethod
    def get_spark_version_id(cls,
                             spark_version: Optional[str] = None) -> JslLibSparkVersionIdentifier:
        """Maps version string to OcrSparkVersionIdentifier
        which is used to navigate a OCR jar/wheel."""
        if not spark_version:
            spark_version = cls.get_installed_pyspark_version_or_latest_compatible()
        else:
            spark_version = spark_version[0:-2].replace(".", "")

        if "23" in spark_version:
            return OcrSparkVersionId.spark23.value
        if "24" in spark_version:
            return OcrSparkVersionId.spark24.value
        if "30" in spark_version:
            return OcrSparkVersionId.spark30.value
        if "32" in spark_version:
            return OcrSparkVersionId.spark32.value
        raise Exception(f'Invalid OCR-Spark-Version-ID:{spark_version}')


class HcLibResolver(JslLibDependencyResolverABC, metaclass=ABCMeta):
    """
    Each JslLibDependencyResolver util must implement the following :
    - get_jar_urls(lib_version,spark_version,Optional[secret])->UrlDependency
    - get_mvn_coordinates(lib_version,spark_version,Optional[secret])->RepoDependency
    - get_python_urls(lib_version,spark_version,Optional[secret],install_type)->UrlDependency
    - get_pypi_identifier(lib_version,spark_version,Optional[secret],install_type)->RepoDependency
    - get_lib_version_i

    """

    has_gpu_jars = True
    product_name = ProductName.healthcare

    @classmethod
    def get_cpu_jar_urls(cls, secret: str, jsl_lib_version: Optional[LibVersionIdentifier] = None,
                         spark_version: Optional[JslLibSparkVersionIdentifier] = None,
                         ) -> UrlDependency:
        """
        Applicable spark version = 23,30,32
        :return:
        """
        if not spark_version:
            spark_version = cls.get_spark_version_id()
        if not jsl_lib_version:
            jsl_lib_version = cls.get_version_from_lib_secret(secret)

        jar_loc = f'https://pypi.johnsnowlabs.com/{secret}' \
                  f'/spark-nlp-jsl-{jsl_lib_version}{spark_version}.jar'
        return UrlDependency(jar_loc, JavaInstallTypes.jar.value)

    @classmethod
    def get_py_urls(cls, jsl_lib_version: Optional[LibVersionIdentifier] = None,
                    install_type: Optional[PyInstallTypes] = PyInstallTypes.wheel, secret: Optional[str] = None,
                    spark_version: Optional[JslLibSparkVersionIdentifier] = None, ) -> UrlDependency:
        """
        install_type_tar = '.tar.gz'
        install_type_wheel = '-py3-none-any.whl'
        Applicable spark version = 23,30,32
        :return:
        """
        if not jsl_lib_version:
            jsl_lib_version = cls.get_version_from_lib_secret(secret)

        install_loc = f'https://pypi.johnsnowlabs.com/{secret}/' \
                      f'spark-nlp-jsl/spark-nlp-jsl-{jsl_lib_version}{install_type.value}'
        if install_type == PyInstallTypes.wheel:
            # For some reason, wheels use a '_' instead of '-'
            install_loc = install_loc.replace(f'spark-nlp-jsl/spark-nlp-jsl-', f'spark-nlp-jsl/spark_nlp_jsl-')

        return UrlDependency(install_loc, install_type.value)

    @classmethod
    def get_spark_version_id(cls, spark_version: Optional[str] = None) -> JslLibSparkVersionIdentifier:
        """Maps version string to NLPSparkVersionIdentifier
        which is used to navigate a NLP jar/wheel."""
        if not spark_version:
            spark_version = cls.get_installed_pyspark_version_or_latest_compatible()
        else:
            spark_version = spark_version[0:-2].replace(".", "")


        if "23" in spark_version:
            return HcSparkVersionId.spark23.value
        if "24" in spark_version:
            return HcSparkVersionId.spark24.value
        if "30" in spark_version or '31' in spark_version:
            return HcSparkVersionId.spark30x_and_spark31x.value
        if "32" in spark_version:
            return HcSparkVersionId.spark32x.value
        raise Exception(f'Invalid NLP-Spark-Version-ID:{spark_version}')


class NlpLibResolver(JslLibDependencyResolverABC, metaclass=ABCMeta):
    """
    Each JslLibDependencyResolver util must implement the following :
    - get_jar_urls(lib_version,spark_version,Optional[secret])->UrlDependency
    - get_mvn_coordinates(lib_version,spark_version,Optional[secret])->RepoDependency
    - get_python_urls(lib_version,spark_version,Optional[secret],install_type)->UrlDependency
    - get_pypi_identifier(lib_version,spark_version,Optional[secret],install_type)->RepoDependency
    - get_lib_version_i

    """

    has_gpu_jars = True
    product_name = ProductName.healthcare

    @classmethod
    def get_installed_jsl_lib_version_or_latest(cls, ) -> LibVersionIdentifier:
        if try_import_lib('sparknlp'):
            import sparknlp
            jsl_lib_version = sparknlp.version()
        else:
            jsl_lib_version = LatestCompatibleProductVersion.spark_nlp.value
        return LibVersionIdentifier(jsl_lib_version)

    @classmethod
    def get_gpu_jar_urls(cls, jsl_lib_version: Optional[LibVersionIdentifier] = None,
                         spark_version: Optional[JslLibSparkVersionIdentifier] = None,
                         secret: Optional[str] = None) -> UrlDependency:
        """
        Applicable spark version = 23,30,32
        :return:
        """
        if not spark_version:
            spark_version = cls.get_spark_version_id()
        if not jsl_lib_version:
            jsl_lib_version = cls.get_installed_jsl_lib_version_or_latest()
        jar_loc = f'https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/jars' \
                  f'/spark-nlp-gpu{spark_version}-assembly-{jsl_lib_version}.jar'

        return UrlDependency(jar_loc, JavaInstallTypes.jar.value)

    @classmethod
    def get_cpu_jar_urls(cls, jsl_lib_version: Optional[LibVersionIdentifier] = None,
                         spark_version: Optional[JslLibSparkVersionIdentifier] = None,
                         secret: Optional[str] = None) -> UrlDependency:
        """
        Applicable spark version = 23,30,32
        :return:
        """
        if not spark_version:
            spark_version = cls.get_spark_version_id()
        if not jsl_lib_version:
            jsl_lib_version = cls.get_installed_jsl_lib_version_or_latest()

        jar_loc = f'https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/jars' \
                  f'/spark-nlp{spark_version}-assembly-{jsl_lib_version}.jar'

        return UrlDependency(jar_loc, JavaInstallTypes.jar.value)

    @classmethod
    def get_py_urls(cls, jsl_lib_version: Optional[LibVersionIdentifier] = None,
                    install_type: Optional[PyInstallTypes] = PyInstallTypes.wheel,
                    spark_version: Optional[JslLibSparkVersionIdentifier] = None,
                    secret: Optional[str] = None) -> UrlDependency:
        """
        install_type_tar = '.tar.gz'
        install_type_wheel = '-py3-none-any.whl'
        Applicable spark version = 23,30,32
        :return:
        """
        offline = False
        if offline:
            # Fallback, we cannot find exact URL withouth internet because Hash is in random version str
            # todo Maybe hardcode the latest?
            return 'https://pypi.org/project/spark-nlp/'

        # Each Release gets new hashcode on each release, we fetch the latest here
        pypi_page = requests.get('https://pypi.org/project/spark-nlp/').text
        if install_type == PyInstallTypes.wheel:
            wheel_rgx = '(?<=https://files.pythonhosted.org).*(?=.any.whl)'
            wheel_url = re.findall(wheel_rgx, pypi_page)[0]
            wheel_url = f'https://files.pythonhosted.org{wheel_url}-any.whl'
            return UrlDependency(wheel_url, install_type.value)
        if install_type == PyInstallTypes.tar:
            tar_rgx = '(?<=https://files.pythonhosted.org).*(?=.tar.gz)'
            tar_url = re.findall(tar_rgx, pypi_page)[0]
            tar_url = f'https://files.pythonhosted.org{tar_url}.tar.gz'
            return UrlDependency(tar_url, install_type.value)

    @classmethod
    def get_spark_version_id(cls, spark_version: Optional[str] = None) -> JslLibSparkVersionIdentifier:
        """Maps version string to NLPSparkVersionIdentifier
        which is used to navigate a NLP jar/wheel."""
        if not spark_version:
            spark_version = cls.get_installed_pyspark_version_or_latest_compatible()
        else:
            spark_version = spark_version[0:-2].replace(".", "")

        if "23" in spark_version:
            return NlpSparkVersionId.spark23.value
        if "24" in spark_version:
            return NlpSparkVersionId.spark24.value
        if "30" in spark_version or '31' in spark_version:
            return NlpSparkVersionId.spark30x_and_spark31x.value
        if "32" in spark_version:
            return NlpSparkVersionId.spark32x.value
        if "40" in spark_version:
            return NlpSparkVersionId.sa.value
        raise Exception(f'Invalid NLP-Spark-Version-ID:{spark_version}')
