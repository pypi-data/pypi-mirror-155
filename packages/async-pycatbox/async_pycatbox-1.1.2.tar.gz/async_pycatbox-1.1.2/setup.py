from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

version = "1.1.2"

setup(
    name="async_pycatbox",
    version=version,
    py_modules=["async_pycatbox"],
    author="Andrew McGrail",
    author_email="andrewjerrismcgrail@gmail.com",
    license="Apache License, Version 2.0, see LICENSE file",
    url="https://github.com/challos/async_pycatbox",
    description="Async version of pycatbox, a Python API wrapper for catbox.moe.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["aiohttp"],
    packages=["async_pycatbox"]
)
