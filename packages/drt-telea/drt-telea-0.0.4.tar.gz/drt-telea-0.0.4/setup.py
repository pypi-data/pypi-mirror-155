import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drt-telea",
    version="0.0.4",
    author="Dmitry Trokhachev",
    author_email="dimiaa573@gmail.com",
    description = "Python implementation of Telea inpaiting method", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimiaa/drt-telea",
    project_urls={
        "Bug Tracker": "https://github.com/dimiaa/drt-telea/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_dir={"telea": "telea"},
    install_requires=[
       'numpy',
    ],
    python_requires=">=3.6,<3.11",
)