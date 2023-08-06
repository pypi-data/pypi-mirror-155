import os

import setuptools
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


setup(
    name='core-changelog-md',
    author="Y. Chudakov",
    author_email="kappasama.ks@gmail.com",
    version=os.getenv('CI_COMMIT_TAG'),
    packages=setuptools.find_packages(),
    package_dir={'core-changelog-md': 'core_changelog_md/'},
    description='core-changelog-md for cli-changelog-md',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/kappasama.ks/openapi_django',
    install_requires=[
          'Django>=3.2.6', 'djantic==0.7.0', 'pydantic==1.9.1'
     ]
)
