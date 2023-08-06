from setuptools import setup, find_packages


setup(
    name='AA-module',
    version='1.1.10',
    license='MIT',
    author="Andreas Bigom, Michael Harborg, Oliver Elmgren & Marcus Presutti",
    author_email='andreasbigom@gmail.com',
    long_description = "This module can be used to perform, evaluate and analyse Conventional Archetypal Analysis, Ordinal Archetypal Analysis and Response Bias Ordinal Archetypal Analysis. The module is developed by Andreas Bigom, Michael Harborg, Marcus Presutti and Oliver Elmgren in a collaboration between the Technical University of Denmark and Copenhagen Business School in order to enable students to analyse human questionnaire data in an effective and meaningful way.",
    description = "Module for performing various archetypal analyses.",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/anden1305/AAM-Module',
    keywords='Archetypal Analysis',
    python_requires = ">=3.9.7",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pandas',
          'numpy',
          'matplotlib',
          'torch',
          'scipy',
          'sklearn',
    ],
)