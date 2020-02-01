import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pointa",
    version="0.2.2",
    author="KRedCell",
    author_email="krov_red_cell@outlook.com",
    description="Pointa Dedicated Server & CLI Based Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KRedCell/Pointa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'gevent==1.4.0',
        'Flask==1.1.1',
        'requests==2.22.0'
    ],
    python_requires='>=3.7'
)