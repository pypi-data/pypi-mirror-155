import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drt-unet",
    version="0.0.4",
    author="Dmitry Trokhachev",
    author_email="dimiaa573@gmail.com",
    description="Neural network for mask creating",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimiaa/drt-unet",
    project_urls={
        "Bug Tracker": "https://github.com/dimiaa/drt-unet/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
       'numpy',
       'tensorflow',
       'matplotlib',
    ],
    python_requires=">=3.6,<3.11",
)