# Fidescls: PII Detection and Classification
_A part of the [greater Fides ecosystem](https://github.com/ethyca/fides)._

[![License][license-image]][license-url]
[![Code style: black][black-image]][black-url]
[![Twitter][twitter-image]][twitter-url]

[![Docker Build](https://github.com/ethyca/fidescls/actions/workflows/docker.yml/badge.svg)](https://github.com/ethyca/fidescls/actions/workflows/docker.yml)
[![CI Checks](https://github.com/ethyca/fidescls/actions/workflows/pr_checks.yml/badge.svg)](https://github.com/ethyca/fidescls/actions/workflows/pr_checks.yml)
[![Publish Docs](https://github.com/ethyca/fidescls/actions/workflows/publish_docs.yml/badge.svg)](https://github.com/ethyca/fidescls/actions/workflows/publish_docs.yml)
[![PyPI](https://github.com/ethyca/fidescls/actions/workflows/publish_package.yaml/badge.svg)](https://github.com/ethyca/fidescls/actions/workflows/publish_package.yaml)

![Fidescls banner](docs/fidescls/docs/img/fidescls.png "Fidescls banner")

## :zap: Overview
Fidescls (*/fee-dhez classify/,* from *Fidēs,* Latin for trust and reliability) is an open-source and extensible machine learning classification engine. Fidescls uses the Fides toolset ([Fidesctl](https://ethyca.github.io/fides/), [Fidesops](https://ethyca.github.io/fidesops/), and [Fideslang](https://ethyca.github.io/fides/language/overview/)) to assist in detecting and labeling potential sources of personal identifiable information, or PII, in your records and databases.

![Fidescls overview](docs/fidescls/docs/img/fidescls-diagram.png "Fidescls overview")
## :rocket: Quick Start

### Requirements
* Docker 12+
* Python 3.8+
* Make
### Getting Started

1. Ensure that the required tools are installed and Docker is running, and clone this repository. 
   
2. From the project's root directory, run the following command:

```
make api
```
   
This will start an instance of the API server, and allow you to begin making requests.

3. Make a post request to the `classify` endpoint:

```
localhost:8765/text/classify
```

<details>
<summary><strong>Sample Payload - Content Classification</strong></summary>

```json
{
    "content": {
        "data": [
            "sample@aol.com",
            "(555) 555-5555",
            "4242-4242-4242-4242"
        ],
        "method_params": {
            "decision_method": "pass-through"
        }
    }
}
```

| field   | description   |
|----|-----|
|`data` | A string, or list of strings, representing the data to be processed. |
| `decision_method` | A value of `pass-through` returns the higher-level PII classifications to which your `data` belongs.|


**Successful Response:**
```json
{
    "content": [
        {
            "input": "sample@aol.com",
            "labels": [
                {
                    "label": "EMAIL_ADDRESS",
                    "score": 1.0,
                    "position_start": 0,
                    "position_end": 14
                },
                {
                    "label": "DOMAIN_NAME",
                    "score": 1.0,
                    "position_start": 7,
                    "position_end": 14
                }
            ]
        },
        {
            "input": "(555) 555-5555",
            "labels": [
                {
                    "label": "PHONE_NUMBER",
                    "score": 0.4,
                    "position_start": 0,
                    "position_end": 14
                }
            ]
        },
        {
            "input": "4242-4242-4242-4242",
            "labels": [
                {
                    "label": "CREDIT_CARD",
                    "score": 1.0,
                    "position_start": 0,
                    "position_end": 19
                }
            ]
        }
    ]
}
```
</details>


<details>
<summary><strong>Sample Payload - Context Classification</strong></summary>

```json 
{
    "context": {
        "data": [
            "email_address",
            "phone_num",
            "credit_card"
            ],
        "method": "similarity",
        "method_params": {
            "possible_targets": [
                "user.derived.identifiable.device.ip_address",
                "user.provided.identifiable.financial.account_number",
                "user.provided.identifiable.contact.email",
                "user.provided.identifiable.contact.phone_number",
                "account.contact.street",
                "account.contact.city",
                "account.contact.state",
                "account.contact.country",
                "account.contact.postal_code"
            ],
            "top_n": 2
        }
    }
}
```

| field   | description   |
|----|-----|
|`data` | A string, or list of strings, representing the data to be processed. |
| `possible_targets` | A list of potential [Data Categories](https://ethyca.github.io/fides/language/taxonomy/data_categories/) to classify your `data` into. |
| `top_n` | The number of closest results to return. |

**Successful Response:**
```json
{
    "context": [
        {
            "input": "email_address",
            "labels": [
                {
                    "label": "user.provided.identifiable.contact.email",
                    "score": 0.791374585498101,
                    "position_start": null,
                    "position_end": null
                },
                {
                    "label": "account.contact.postal_code",
                    "score": 0.7402522077965934,
                    "position_start": null,
                    "position_end": null
                }
            ]
        },
        {
            "input": "phone_num",
            "labels": [
                {
                    "label": "user.provided.identifiable.contact.phone_number",
                    "score": 0.5770164988785474,
                    "position_start": null,
                    "position_end": null
                },
                {
                    "label": "account.contact.postal_code",
                    "score": 0.44817613132976103,
                    "position_start": null,
                    "position_end": null
                }
            ]
        },
        {
            "input": "credit_card",
            "labels": [
                {
                    "label": "user.provided.identifiable.financial.account_number",
                    "score": 0.5742921242220389,
                    "position_start": null,
                    "position_end": null
                },
                {
                    "label": "account.contact.postal_code",
                    "score": 0.5587338672966902,
                    "position_start": null,
                    "position_end": null
                }
            ]
        }
    ]
}
```
</details>

> To learn more about the difference between Context and Content Classification, see the [Classifiers Guide](docs/fidescls/docs/guides/classifiers.md).

You've now successfully begun classifying PII!

## :book: Learn More

The Fides core team is committed to providing a variety of documentation to help get you started using Fidescls.  As such, all interactions are governed by the [Fides Code of Conduct](https://ethyca.github.io/fides/community/code_of_conduct/).

### Documentation

For more information on getting started with Fidescls and the Fides ecosystem of open source projects, check out our documentation: 

- Documentation: https://ethyca.github.io/fidescls/
- Guides: https://ethyca.github.io/fidescls/guides/classifiers/

### Support

Join the conversation on [Slack](https://fid.es/join-slack) and [Twitter](https://twitter.com/ethyca)!

## :balance_scale: License

The Fides ecosystem of tools ([Fidescls](https://github.com/ethyca/fidescls), [Fidesops](https://github.com/ethyca/fidesops) and [Fidesctl](https://github.com/ethyca/fides)) are licensed under the [Apache Software License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
Fides tools are built on [Fideslang](https://github.com/ethyca/privacy-taxonomy), the Fides language specification, which is licensed under [CC by 4](https://github.com/ethyca/privacy-taxonomy/blob/main/LICENSE). 

Fides is created and sponsored by [Ethyca](https://ethyca.com): a developer tools company building the trust infrastructure of the internet. If you have questions or need assistance getting started, let us know at fides@ethyca.com!


[license-image]: https://img.shields.io/:license-Apache%202-blue.svg
[license-url]: https://www.apache.org/licenses/LICENSE-2.0.txt
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black/
[twitter-image]: https://img.shields.io/twitter/follow/ethyca?style=social
[twitter-url]: https://twitter.com/ethyca
