from setuptools import setup

# parse requirements from requirements.txt

with open(f"/home/vaibhav/Documents/Projects/Accoladez/SubscriptionModel/cli/requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='accomate',
    url='https://github.com/Accoladez/Accomate',
    version='1.0.0',
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
