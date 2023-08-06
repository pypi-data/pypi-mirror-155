from setuptools import setup, find_packages


VERSION = '0.0.12'
DESCRIPTION = 'rpc aggregation'
LONG_DESCRIPTION = 'rpc aggregation.'

# Setting up
setup(
    name="dcentrapi",
    version=VERSION,
    author="Dcentralab (Niv Shitrit)",
    author_email="<niv@dcentralab.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)