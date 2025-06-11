import pathlib

import setuptools

REPO = pathlib.Path(__file__).parent

README = (REPO / "readme.md").read_text()

setuptools.setup(
    name="pysintegra",
    version="1.0.0",
    author="Felipe Correa",
    author_email="eu@felps.dev",
    description="Modern SINTEGRA magnetic file generator and parser with Pydantic models",  # noqa: E501
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/felps-dev/pysintegra",
    project_urls={"Bug Tracker": "https://github.com/felps-dev/pysintegra/issues"},
    license="LGPL",
    packages=["pysintegra"],
    install_requires=[
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ]
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
