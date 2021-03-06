import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/admissions-cohort-manager>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'cohort_manager/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/admissions-cohort-manager"
setup(
    name='Admissions Cohort Manager',
    version=VERSION,
    packages=['cohort_manager'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'django>=2.2,<2.3',
        'UW-Django-SAML2>=1.4,<2.0',
        'django-webpack-loader<1.0',
        'UW-RestClients-AdSel==1.7.8',
        'django-userservice<4.0,>3.1'
        'pytz==2019.3',
        'django-cookies-samesite',
        'psycopg2==2.8.6'

    ],
    license='Apache License, Version 2.0',
    description='A tool for managing cohorts',
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
