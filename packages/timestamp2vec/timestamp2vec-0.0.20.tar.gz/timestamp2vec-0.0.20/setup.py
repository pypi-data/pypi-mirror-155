from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.20'
DESCRIPTION = 'Vectorizing Timestamps by means of a Variational Autoencoder'

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="timestamp2vec",
    version=VERSION,
    author="Gideon Rouwendaal",
    author_email="<gideon.rouwendaal@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'timestamp2vec': ['important_variables/*', 'encoder_VAE/*', 'encoder_VAE/assests/*', 'encoder_VAE/variables/*']},
    include_package_data=True,
    install_requires=['keras', 'matplotlib', 'numpy', 'tensorflow', 'pathlib', 'seaborn', 'pandas', 'datetime'],
    keywords=['python', 'vector', 'time', 'timestamps'],
    url = 'https://github.com/GideonRouwendaal/Timestamp2Vec',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# python setup.py sdist bdist_wheel
# twine upload dist/*