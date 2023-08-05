from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="cgcsdk",
    version="0.1.5",
    description="Comtegra GPU Cloud REST API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Comtegra/cgc",
    author="Comtegra AI Team",
    author_email="info@comtegra.pl",
    keywords=["cloud", "sdk"],
    license="BSD 2-clause",
    packages=find_packages(),
    package_data={"src": [".env"]},
    py_modules=["src/cgc"],
    install_requires=[
        "click",
        "python-dotenv",
        "tabulate",
        "pycryptodomex",
        "paramiko>=2.11",
        "statsd",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "cgc = src.cgc:cli",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
