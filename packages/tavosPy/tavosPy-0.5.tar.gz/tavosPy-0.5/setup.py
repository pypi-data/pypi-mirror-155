import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tavosPy",
    version="0.5",
    author="Juraj Nyíri",
    author_email="juraj.nyiri@gmail.com",
    description="Processes water outages from Tavos and provides them in a object with proper types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JurajNyiri/tavosPy",
    packages=setuptools.find_packages(),
    install_requires=["requests", "pyquery"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
