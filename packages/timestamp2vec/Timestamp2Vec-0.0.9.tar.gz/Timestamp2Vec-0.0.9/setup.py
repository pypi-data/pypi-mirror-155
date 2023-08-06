from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'Vectorizing Timestamps by means of a Variational Autoencoder'

# Setting up
setup(
    name="Timestamp2Vec",
    version=VERSION,
    author="Gideon Rouwendaal",
    author_email="<gideon.rouwendaal@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(include=["Timestamp2Vec", "encoder_VAE", "important_variables"]),
    install_requires=['keras', 'matplotlib', 'numpy', 'tensorflow', 'pathlib', 'seaborn', 'pandas', 'datetime'],
    keywords=['python', 'vector', 'time', 'timestamps'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)