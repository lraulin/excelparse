import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='excelparse',
    version='0.0.1',
    entry_points={
        'console_scripts': ['excelparse=excelparse.main:main'],
    },
    author="Lee Raulin",
    author_email="leeraulin@gmail.com",
    description="Show current weather from OpenWeather API in console.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lraulin/excelparse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
