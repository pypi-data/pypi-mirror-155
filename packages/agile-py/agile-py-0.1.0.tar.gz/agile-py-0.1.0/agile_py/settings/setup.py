from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="example-package",  # name of the package
    version="0.0.1",  # version of the package
    author="Example Author",  # author of the package
    author_email="example@example.com",  # email of the author
    description="example description",  # description of the package
    url="https://example.com/example-package",  # url of the package
    packages=setuptools.find_packages(),
    entry_points={},  # entry points for the package
    include_package_data=True,  # include package data
    package_data={},  # package data to be included
    python_requires=">=3.7",  # python version required
    license="Apache Software License (Apache-2.0)",  # license of the package
    install_requires=[],  # dependencies of the package
    long_description=long_description,  # long description of the package
    long_description_content_type="text/markdown",  # content type of the long description
)
