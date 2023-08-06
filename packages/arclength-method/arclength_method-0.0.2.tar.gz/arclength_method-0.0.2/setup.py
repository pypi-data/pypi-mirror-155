from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="arclength_method",
    version="0.0.2",
    author="Konstantin Sokolovskiy",
    author_email="kosokolovsky@gmail.com",
    description="Arc Length Method for non-linear FEM",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/kosokolovskiy/FEM_studywork_3.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)