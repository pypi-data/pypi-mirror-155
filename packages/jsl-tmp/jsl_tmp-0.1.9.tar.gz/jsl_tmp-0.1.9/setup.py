
print("WASSUPPPPP")
from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

REQUIRED_PKGS = [
    'nlu',
    'pyspark==3.0.1', # TODO MUST BE OPTIONAL/ SMARTY HANDLED, NOT RUN IF DATABRICKS!!!
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
        "lol": ["plotly"],
    },

    version='0.1.9',
    description='John Snow Labs NLU provides state of the art algorithms for NLP&NLU with 4000+ of pretrained models in 200+ languages. It enables swift and simple development and research with its powerful Pythonic and Keras inspired API. It is powerd by John Snow Labs powerful Spark NLP library.',
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
