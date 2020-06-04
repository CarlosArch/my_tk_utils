import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my-tkutils-CarlosArch", # Replace with your own username
    version="0.0.1",
    author="Carlos Daniel Archundia Cejudo",
    author_email="carlos_arch@hotmail.com",
    description="Utilities for tkinter applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CarlosArch/my_tk_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.3',
)
