import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drt-mask-generator",
    version="0.0.5",
    author="Dmitry Trokhachev",
    author_email="dimiaa573@gmail.com",
    description="Tool for mask creating",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimiaa/drt-mask-generator",
    project_urls={
        "Bug Tracker": "https://github.com/dimiaa/drt-mask-generator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_dir={"maskGenerator": "maskGenerator"},
    install_requires=[
       'PySide2',
       'shiboken2',
    ],
    python_requires=">=3.6,<3.11",
)