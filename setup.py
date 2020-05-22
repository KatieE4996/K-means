import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="K-means-pkg-Katie_E4996", 
    version="0.0.1",
    author="Katie Easlon",
    author_email="kleaslon@gmail.com",
    description="an implementation of the K-means algorithm only using Numpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KatieE4996/K-means.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
