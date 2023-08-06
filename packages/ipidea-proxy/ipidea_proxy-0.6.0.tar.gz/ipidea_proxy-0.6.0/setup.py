import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipidea-proxy",
    version="0.6.0",
    author="Pinclr Coders",
    author_email="coding@pinclr.com",
    description="Python Client for Ipidea Proxy Service API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src"),
    package_data={'': ['*.py']},
    url="https://github.com/pinclr/ipidea-proxy",
    install_requires = [],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
