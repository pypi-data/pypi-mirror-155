import setuptools

#Genrate long description using readme file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppigrf",
    version="1.0.0",
    author="Karl Laundal",
    author_email="readme@file.md",
    description="Pure Python IGRF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'numpy>=0.13.1',
    ],
    package_dir={"": "src"},
    package_data={'':['IGRF13.shc']},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
