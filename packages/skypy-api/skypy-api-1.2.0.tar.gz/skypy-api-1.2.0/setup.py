import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="skypy-api",
    url="https://github.com/FuchsCrafter/skypy",
    version="1.2.0",
    author="FuchsCrafter",
    license="GPL2",
    description="Framework to connect to the Hypixel Skyblock API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
    install_requires=["requests", "json"]
)
