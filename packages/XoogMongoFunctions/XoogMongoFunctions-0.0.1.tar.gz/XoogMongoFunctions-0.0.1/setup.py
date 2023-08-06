from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'convert a Pandas DataFrame into a MongoDB document'

# Setting up
setup(
    name="XoogMongoFunctions",
    version=VERSION,
    author="Paweł Lachowski",
    author_email="<pawel.lachowski@xoog.pl>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
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
