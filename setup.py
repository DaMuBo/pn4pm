import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pn4pm_nano", # package name
    version="0.0.4.1",
    author="Daniel Muller",
    author_email="daniel.mueller@damu-analytics.com",
    description="A small package for handling process models given as lists with their own row number and the row number of previous activity"
                "Returning a Petri Net for Process Mining / Conformance Checks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DaMuBo/pn4pm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)