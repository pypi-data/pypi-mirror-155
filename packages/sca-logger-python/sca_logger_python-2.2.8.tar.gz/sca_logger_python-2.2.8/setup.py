from setuptools import setup

setup(
    name='sca_logger_python',
    version='2.2.8',
    description='Provides a logger client, more specific to work with AWS Lambda and log to Kinesis',
    author='Venkatesh Kara',
    author_email='vkara@tesla.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=['sca_logger'],
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)
