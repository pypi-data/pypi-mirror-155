from setuptools import setup, find_packages
from os import path
import codecs


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'PYPIREADME.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(rel_path):
    here = path.abspath(path.dirname(__file__))
    with codecs.open(path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Setup
setup(
    name='mauspaf',
    author='M. Nuño',
    version=get_version("./src/mauspaf/__init__.py"),
    description='Mass properties analysis.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/mnn/mauspaf',
    author_email='mnunos@outlook.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
    ],
    keywords='',
    packages=find_packages(
        where='src',
        exclude=['tests'],
    ),
    package_dir={"": "src"},
    python_requires='>=3.6',
    install_requires=[x.strip() for x in
                      open('./requirements/use.txt').readlines()],
    extras_require={},
    entry_points={
        'console_scripts': ['mauspafgui=mauspaf.application:main']
        },
    package_data={'': ['PYPIREADME.rst', 'LICENSE', './requirements/use.txt']},
    include_package_data=True,
    project_urls={
        'Documentation': 'https://mnn.gitlab.io/mauspaf/',
        'Source': 'https://gitlab.com/mnn/mauspaf',
        'Bug Reports': 'https://gitlab.com/mnn/mauspaf/-/issues',
    },
    py_modules=['resources_rc'],
)
