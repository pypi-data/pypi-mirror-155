from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="earlybyte-mvv",
    version="0.0.5",
    author="Remo Hoeppli",
    author_email="remo.hoeppli@earlybyte.ch",
    license="MIT License",
    description="earlybtyte mission, vision, and value statement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.earlybyte.ch",
    py_modules=["earlybyte"],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        earlybyte=earlybyte:main
    """,
)
