from ensurepip import version
import pathlib
from setuptools import find_packages, setup

setup(
    name='apiintercambiador',
    version='0.0.3',
    description='Librería para transferir información entre API Intercambiador y las fuentes de datos.' ,
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    author='Marc Güell Jiménez',
    author_email='mguell@tridenia.com',
    url='',
    license='MIT',
    py_modules=["apiintercambiador"],
    package_dir={'':'src'},
    install_requires=[
        'requests'
    ]
)