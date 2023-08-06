import setuptools, mp3toolsce

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mp3toolsce", # Replace with your own username
    version=mp3toolsce.__version__,
    author="Carsten Engelke",
    author_email="carsten.engelke@gmail.com",
    description="Tools for merging mp3 files using foobar2000, e.g. audiobooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carsten-engelke/mp3-tools",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'mp3toolsce = mp3toolsce.mp3tools:main',
        ],
    },    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["autopep8>=1", "natsort>=7", "pycodestyle>=2", "pynput>=1", "six>=1"]
)