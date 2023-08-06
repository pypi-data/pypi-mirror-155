import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="xlinjietool",
    version="0.0.1",
    author="Linjie Xing",
    author_email="jin.951107@gmail.com",
    description="工具库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xlj997/xlinjietool",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'xlinjietool=xlinjietool.converter:run'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)