# Installation from PyPI

Fidescls is available as an independent package [published on PyPI](https://pypi.org/project/fidescls/).

## Basic Installation

To install Fidescls as a python package, run:
```sh
pip install fidescls
```

This will install the latest version that has been published to PyPi.

### Dependencies
Fidescls depends on [Spacy trained pipelines](https://spacy.io/models/en)
which must be installed after running the pip install mentioned above.
In particular, the required trained pipelines are: `en_core_web_sm`,
and `en_core_web_lg`.  These can be installed by executing the following
commands in the environment in which Fidescls has been installed:

```bash
python -m spacy download en_core_web_sm

python -m spacy download en_core_web_lg
```

## Next Steps
Once installed, you may use the [fidescls module](../guides/module.md) to begin classifying PII within your own projects.