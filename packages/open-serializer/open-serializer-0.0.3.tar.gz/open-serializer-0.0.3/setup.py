from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="open-serializer",
    version="0.0.3",
    author="Jia-Yau Shiau",
    author_email="jiayau.shiau@gmail.com",
    description="python object serializer",
    url="https://github.com/Janus-Shiau/open-serializer",
    packages=setuptools.find_packages(),
    entry_points={},
    include_package_data=False,
    python_requires=">=3.7",
    license="LICENSE",
    install_requires=["rich", "ruamel.yaml", "toml"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
