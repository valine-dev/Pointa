import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pointa",
    version="0.0.1",
    author="KRedCell",
    author_email="krov_red_cell@outlook.com",
    description="Pointa Dedicated Server & Demo CLI Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KRedCell/Pointa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)