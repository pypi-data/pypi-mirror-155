from setuptools import setup, find_packages
from pypandoc import convert_file

setup(
    name='anutils',
    version='0.1.1',
    license='MIT',
    author="Aaron Ning",
    author_email='foo@bar.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    description='Private utilities of A. Ning. ',
    long_description = convert_file('README.md', 'rst'), 

    url='https://github.com/AaronNing/utils',
    keywords='anutils',
    install_requires=[
        'scipy',
        'numpy',
        'pandas', 
        'matplotlib',
        'seaborn', 
        'scanpy', 
        ],
)