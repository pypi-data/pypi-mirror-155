import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytest-codecarbon",
    version="1.0.0",
    author="Alex H. Room",
    author_email="alex.room@btinternet.com",
    description="Pytest plugin for measuring carbon emissions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexhroom/pytest-codecarbon",
    project_urls={
        "Bug Tracker": "https://github.com/alexhroom/pytest-codecarbon/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    py_modules=["pytest_codecarbon"],
    python_requires=">3.6",
    install_requires=[
        "pytest",
        "codecarbon",
        "pandas",
    ],
    entry_points={"pytest11": ["codecarbon=pytest_codecarbon"]},
)
