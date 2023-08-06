from setuptools import setup

setup(
    name="anvil-stubs",
    version="0.0.1",
    packages=["anvil-stubs"],
    package_data={
        "": ["*/*.pyi"],
        "anvil-stubs": ["*.pyi"],
    },
    install_requires=[
        "anvil-uplink",
    ],
)
