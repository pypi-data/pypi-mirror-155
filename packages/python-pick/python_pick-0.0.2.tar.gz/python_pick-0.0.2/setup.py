import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_pick",
    version="0.0.2",
    author="Coder10",
    author_email="coder10@pikit.com",
    description="Python pick, pick module on py code without use terminal !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheGamer548/Pikkit",
    project_urls={
        "Source-code": "https://github.com/TheGamer548/Pikkit",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"https://github.com/TheGamer548/Pikkit": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)