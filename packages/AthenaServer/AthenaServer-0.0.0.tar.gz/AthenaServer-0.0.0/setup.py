# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import setuptools

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def readme_handler() -> str:
    with open("README.md", "r") as readme_file:
        return readme_file.read()

def version_handler() -> str:
    # ------------------------------------------------------------------------------------------------------------------
    version = 0,0,0 # <-- DEFINE THE VERSION IN A TUPLE FORMAT HERE
    # ------------------------------------------------------------------------------------------------------------------
    version_str = ".".join(str(i) for i in version)

    with open("src/AthenaServer/_info/_v.py", "w") as file:
        file.write(f"VERSION='{version_str}'")

    return version_str

setuptools.setup(
    name="AthenaServer",
    version=version_handler(),
    author="Andreas Sas",
    author_email="",
    description="A general server system for Directive Athena Applications",
    long_description=readme_handler(),
    long_description_content_type="text/markdown",
    url="https://github.com/DirectiveAthena/AthenaServer",
    project_urls={
        "Bug Tracker": "https://github.com/DirectiveAthena/AthenaServer/issues",
    },
    license="GPLv3",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
    ]
)