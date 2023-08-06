from setuptools import setup

# parse requirements from requirements.txt

required_packages = '''
astroid==2.11.6
attrs==21.4.0
autopep8==1.6.0
beautifulsoup4==4.11.1
boto3==1.24.2
botocore==1.27.2
build==0.8.0
certifi==2022.5.18.1
cffi==1.15.0
charset-normalizer==2.0.12
click==8.1.3
cloudflare==2.9.10
cryptography==37.0.2
dill==0.3.5.1
docker==5.0.3
feedparser==6.0.10
fire==0.4.0
flake8==4.0.1
html2text==2020.1.16
idna==3.3
isort==5.10.1
jmespath==1.0.0
jsonlines==3.0.0
lazy-object-proxy==1.7.1
mccabe==0.6.1
packaging==21.3
pep517==0.12.0
platformdirs==2.5.2
pycodestyle==2.8.0
pycparser==2.21
pycryptodome-test-vectors==1.0.8
pycryptodomex==3.14.1
pyflakes==2.4.0
pylint==2.14.1
pymongo==4.1.1
pyparsing==3.0.9
python-dateutil==2.8.2
python-dotenv==0.20.0
PyYAML==6.0
randomname==0.1.5
requests==2.27.1
s3transfer==0.6.0
sgmllib3k==1.0.0
six==1.16.0
soupsieve==2.3.2.post1
termcolor==1.1.0
toml==0.10.2
tomli==2.0.1
tomlkit==0.11.0
typer==0.4.1
urllib3==1.26.9
websocket-client==1.3.2
wrapt==1.14.1
'''

requirements = required_packages.split("\n")

# remove blank lines
requirements = [x for x in requirements if x]

setup(
    name='accomate',
    url='https://github.com/Accoladez/Accomate',
    version='1.0.5',
    description='Accoladez + Automate = Accomate',
    author='Accoladez',
    author_email='vaibhav@itday.in',
    packages=['accomate', 'accomate.utils', 'accomate.aws'],
    package_data={'accomate': ['conf/*', "conf/nginx/*", 'scripts/*']},
    install_requires=requirements,
    entry_points={
        'console_scripts': ['accomate=accomate:app',
                            'rees3=accomate:app'],
    },
)
