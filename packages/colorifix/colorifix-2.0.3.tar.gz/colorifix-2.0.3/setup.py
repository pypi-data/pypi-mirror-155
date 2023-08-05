import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorifix",
    version="2.0.3",
    author="Moris Doratiotto",
    author_email="moris.doratiotto@gmail.com",
    description="A python module to color your terminal output life",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mortafix/Colorifix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    keywords=["color", "bash", "terminal", "crayons"],
)
