import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DART-OhGreat",
    version="0.0.2",
    author="Dimitrios Ieronymakis",
    author_email="dimitris.ieronymakis@gmail.com",
    description="A python implementation of the DART algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OhGreat/DART_python",
    project_urls={
        "Bug Tracker": "https://github.com/OhGreat/DART_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)