import setuptools

setuptools.setup(
  name="transmute-common",
  version="0.0.14",
  author="Adrian Flannery",
  author_email="aflanry@gmail.com",
  description="A package to support ETL creation within Transmute",
  url="https://github.com/finnor/transmute-common-py",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.8',
)