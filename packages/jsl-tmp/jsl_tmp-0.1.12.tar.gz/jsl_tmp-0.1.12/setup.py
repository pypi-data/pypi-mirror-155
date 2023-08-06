print("WASSUPPPPP I AM SETUP.PY BBBBBBBBBBBBBBBBBITCH!")
from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

REQUIRED_PKGS = [
    'nlu', # adds spark-nlp
    # 'pyspark==3.0.1', # TODO MUST BE OPTIONAL/ SMARTY HANDLED, NOT RUN IF DATABRICKS!!!
    # TODO , install pyspark ON THE FLY, if ENV IS NOT DATABRICKS and PYSPARK MISSING?
    'numpy',
    'pyarrow>=0.16.0',
    'pandas>=1.3.5',
    'dataclasses'
]
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    name='jsl_tmp',  
    extras_require={
        "full": ["plotly"],
        "lol": ["plotly"],
    },

    version='0.1.12',
    description='JSL-LIB TODO placeholder',
    long_description=long_description,
    install_requires=REQUIRED_PKGS,
    long_description_content_type='text/markdown',
    url='http://nlu.johnsnowlabs.com',
    author='John Snow Labs',
    author_email='christian@johnsnowlabs.com',
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='NLP spark development NLU ',
    packages=find_packages(exclude=['test*', 'tmp*']),
    include_package_data=True

)
