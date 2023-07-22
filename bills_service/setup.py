# setup.py


from setuptools import setup, find_packages

setup(
    name='bills_service',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'mysqlclient'
    ],
    test_suite='tests',
)

