from setuptools import setup, find_packages

# pylint: disable=all
"""
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload dist/*
export CURL_CA_BUNDLE="" && python -m twine upload --repository-url https://nexus-ci.corp.dev.vtb/repository/puos-pypi-lib/ dist/*
"""

REQUIRED = [
    'aiohttp>=3.6.2',
    'aio_pika>=6.6.1',
    'simplejson>=3.17.2',
    'requests>=2.18.0',
    'ujson>=2.0.2',
    'envparse>=0.2.0',
    'vtb-py-logging>=1.1.11',
    'vtb-http-interaction>=0.1.7',
    'asgiref>=3.5.0',
    'vtb_cloud_sdk==1.13'
]

setup(
    name='vtb-state-service-utils',
    version='1.8.0',
    packages=find_packages(exclude=['tests']),
    package_data={'': ['datafiles/*.json']},
    include_package_data=True,
    url='https://bitbucket.org/Michail_Shutov/state_service_utils',
    license='',
    author=' Mikhail Shutov',
    author_email='michael-russ@yandex.ru',
    description='utils for VTB state service',
    install_requires=REQUIRED,
    extras_require={
        'test': [
            'pytest',
            'pytest-env',
            'pytest-dotenv',
            'pytest-mock',
            'pylint',
            'pytest-asyncio',
            'python-dotenv',
            'mq-misc'
        ]
    }
)
