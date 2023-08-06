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
    install_requires=["setuptools>=57.0.0", 'packaging>=21.3', "pytest>=7.1.2"],
    python_requires='>=3.8',
    classifiers=["Programming Language :: Python :: 3"]
)
