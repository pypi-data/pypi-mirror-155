from setuptools import setup
from os import path

longDescription = None

with open("README.md", encoding="utf-8") as file:
    longDescription = file.read()

setup(
   name="PupilPathApi",
   version="1.0.0",
   description="The one and only PupilPath api wrapper",
   long_description=longDescription,
   long_description_content_type="text/markdown",
   author="Dark Studios",
   packages=["PupilPathApi"],
   install_requires=["bs4", "requests"],
)
