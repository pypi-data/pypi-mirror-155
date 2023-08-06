from setuptools import setup, find_packages

setup(
    name='anutils',
    version='0.1.0',
    license='MIT',
    author="Aaron Ning",
    author_email='foo@bar.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
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