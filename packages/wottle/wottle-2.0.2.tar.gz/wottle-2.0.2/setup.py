from setuptools import setup


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

requirements = ["aiohttp"]

setup(
    name="wottle",
    version="2.0.2",
    author="qxtony",
    author_email="qxtonydev@gmail.com",
    description="Asynchronous library for getting the weather forecast in the desired city.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qxtony/wottle",
    packages=["wottle"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)