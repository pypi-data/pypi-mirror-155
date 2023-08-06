import setuptools

with open("README.md", "r") as fhandle:
    long_description = fhandle.read() # Your README.md file will be used as the long description!

setuptools.setup(
    name="autoball", # Put your username here!
    version="1.0.0", # The version of your package!
    author="Fruitsy", # Your name here!
    description="This module simply just automatically generates random 8ball choices.", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    url="https://github.com/ItzBlueBerries/Autoball",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.8.2', # The version requirement for Python to run your package!
)
