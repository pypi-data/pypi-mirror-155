import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nester-charley",
    version="0.0.7",
    author="charleyzheng",
    author_email="3216057905@qq.com",
    description="A simple printer of nested lists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.baidu.com",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)