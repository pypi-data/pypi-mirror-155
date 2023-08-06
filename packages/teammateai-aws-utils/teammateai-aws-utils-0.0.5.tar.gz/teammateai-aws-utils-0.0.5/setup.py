from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'AWS utils package'
LONG_DESCRIPTION = 'A package that makes it easy to interact with aws services across multipl products.'

setup(
    name="teammateai-aws-utils",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Jothi Panchatcharam",
    author_email="jothi@teammateai.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'dynamodb-json',
        'boto3',
        'botocore'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3.6',
    ]
)
