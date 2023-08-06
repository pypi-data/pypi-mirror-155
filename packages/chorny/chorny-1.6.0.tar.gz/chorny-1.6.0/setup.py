from pathlib import Path

from setuptools import setup

project_root = Path(__file__).parent


with open(project_root / "README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="chorny",
    description="Loader of Black to ensure Athenian's code formatting conventions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.6.0",
    license="MIT",
    author="Athenian",
    author_email="vadim@athenian.co",
    url="https://github.com/athenianco/chorny",
    py_modules=["chorny"],
    keywords=["black"],
    install_requires=["black"],
    package_data={
        "": [
            "README.md",
        ],
    },
    entry_points={
        "console_scripts": [
            "chorny=chorny:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)
