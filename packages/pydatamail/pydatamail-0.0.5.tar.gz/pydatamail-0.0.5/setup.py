"""
Setuptools based setup module
"""
from setuptools import setup, find_packages
from pathlib import Path
import versioneer


setup(
    name='pydatamail',
    version=versioneer.get_version(),
    description='pydatamail - a python module to apply data science principles to email processing',
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/pyscioffice/pydatamail',
    author='Jan Janssen',
    author_email='jan.janssen@outlook.com',
    license='BSD',
    packages=find_packages(exclude=["*tests*"]),
    install_requires=[
        'tqdm>=4.64.0',
        'pandas>=1.4.2',
        'sqlalchemy>=1.4.37',
        'numpy>=1.22.4',
        'matplotlib>=3.5.2',
        'scikit-learn>=1.1.1'
    ],
    cmdclass=versioneer.get_cmdclass()
)
