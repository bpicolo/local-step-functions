from distutils.core import setup

setup(
    name='local-step-functions',
    version='0.1dev',
    packages=['local_step_functions',],
    install_requires=[
        'arrow',
        'boto3',
        'flask',
        'Flask-SQLAlchemy',
        'jsonpath',
        'sqlalchemy',
    ],
    license='MIT',
    long_description=''
)
