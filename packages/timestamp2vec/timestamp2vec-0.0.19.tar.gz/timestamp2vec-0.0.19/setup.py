from setuptools import setup, find_packages

VERSION = '0.0.19'
DESCRIPTION = 'Vectorizing Timestamps by means of a Variational Autoencoder'

# Setting up
setup(
    name="timestamp2vec",
    version=VERSION,
    author="Gideon Rouwendaal",
    author_email="<gideon.rouwendaal@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    package_data={'timestamp2vec': ['important_variables/*', 'encoder_VAE/*', 'encoder_VAE/assests/*', 'encoder_VAE/variables/*']},
    include_package_data=True,
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