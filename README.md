# Falcon on AWS Lambda

This repository is source code for a proof of concept running Falcon in AWS Lambda. The whole shebang is triggered by AWS API Gateway.

***WARNING***: API Gateway _must_ be HTTP and serving payload version 1.0 (2.0 is incompatible with the `aswgi` adapter).

## Requirements

- AWS Account (haha)
- Python >=3.8.2
- `pipenv`

## Usage

- Clone repository
- `cd falcon-on-aws-lambda && pipenv install --dev`
- Edit `lambda-congif.toml` to use your `function_name` and `profile`
  - `profile` must have correct permissions & match a configured AWS CLI profile
- To deploy: `doit`
