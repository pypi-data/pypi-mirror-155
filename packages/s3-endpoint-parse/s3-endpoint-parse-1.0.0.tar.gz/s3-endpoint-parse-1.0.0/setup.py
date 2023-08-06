from setuptools import find_packages, setup

setup(
    name='s3-endpoint-parse',
    packages=find_packages(include=['s3_endpoint_parse']),
    version='1.0.0',
    description='Flexibly extract information from S3 endpoint URL/URI strings',
    author='Patrick C. Kilgore',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.0.0'],
    test_suite='tests',
)
