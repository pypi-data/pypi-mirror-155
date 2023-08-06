from setuptools import setup, find_packages

version = "1.0.14"
description = "A basic module for statistic works!"
with open("README.md", 'r', encoding = 'utf-8') as fh:
    lond_description = fh.read()

setup(name = "plotstats",
      version = version,
      author = "Amirreza Soltani",
      author_email = "charleswestmorelandPB1@gmail.com",
      description = description,
      long_description = lond_description,
      long_description_content_type="text/markdown",
      packages = find_packages(where = "src"),
      install_requires = ['numpy', 'pandas', 'matplotlib'],
      keywords = ['python', 'statistics', 'visualization', 'data grouping', 'plenty', 'relative plenty', 'batch centers'],
      classifiers = ['Programming Language :: Python :: 3',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: Unix',
                    'Operating System :: MacOS :: MacOS X',
                    'Operating System :: Microsoft :: Windows'],
      package_dir={"": "src"},  
      python_requires = '>=3.6'
 )