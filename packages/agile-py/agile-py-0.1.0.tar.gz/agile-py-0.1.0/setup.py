from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="agile-py",
    version="0.1.0",
    author="Jia-Yau Shiau",
    author_email="jiayau.shiau@gmail.com",
    description="agile python project utilities",
    url="https://github.com/Janus-Shiau/agile-py",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "apy=agile_py.cli.cli:cli",
        ]
    },
    include_package_data=True,
    package_data={
        "": [
            "settings/*.toml",
            "settings/*.yaml",
            "settings/*.json",
            "settings/*.py",
            "settings/gitignore",
            "settings/*.md" "scripts/*.sh",
            "settings/license/*",
            "settings/ga/*yml",
        ],
    },
    python_requires=">=3.7",
    license="Apache Software License (Apache-2.0)",
    install_requires=["click", "rich", "black", "isort", "ruamel.yaml", "toml", "open-serializer"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
