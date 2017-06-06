from setuptools import setup

setup(
    name='local-step-functions',
    version='0.1dev',
    packages=['local_step_functions', ],
    install_requires=[
        'arrow',
        'boto3',
        'Flask',
        'Flask-SQLAlchemy',
        'jsonpath-ng',
        'sqlalchemy',
    ],
    license='MIT',
    long_description=''
)
