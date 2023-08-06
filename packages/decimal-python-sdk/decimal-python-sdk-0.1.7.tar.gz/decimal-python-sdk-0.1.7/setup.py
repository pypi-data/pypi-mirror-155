import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="decimal-python-sdk",
    version="0.1.7",
    author="DecimalTeam",
    description="",
    long_description=long_description,
    install_requires=['asn1crypto==1.4.0', 'base58==2.0.0', 'base58check==1.0.2', 'bech32==1.2.0', 'bip32==0.0.8', 'cached-property==1.5.2', 'certifi==2020.11.8', 'cffi==1.14.3', 'chardet==3.0.4', 'coincurve==13.0.0', 'cytoolz==0.11.0', 'ecdsa==0.16.1', 'eth-hash==0.3.1', 'eth-typing==2.2.2', 'eth-utils==1.10.0', 'ethereum==2.3.2', 'future==0.18.2', 'idna==2.10', 'mnemonic==0.19', 'mypy-extensions==0.4.3', 'pbkdf2==1.3', 'py-ecc==5.1.0', 'pyaes==1.6.1', 'pycparser==2.20', 'pycryptodome==3.9.9', 'pycryptodomex==3.9.9', 'pyethash==0.1.27', 'pysha3==1.0.2', 'PyYAML==5.4.1', 'repoze.lru==0.7', 'requests==2.25.0', 'rlp==1.2.0', 'rpl==1.8.1', 'scrypt==0.8.17', 'six==1.15.0', 'sslcrypto==2.0', 'toolz==0.11.1', 'urllib3==1.26.2'],
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/decimalteam/decimal-python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
