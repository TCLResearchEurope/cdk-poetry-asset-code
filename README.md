# PoetryAssetCode for AWS CDK

A custom AWS CDK construct that integrates Poetry for building Python Lambda function packages, automating the process of dependency resolution, packaging, and deployment preparation.

## Features

- **Poetry Integration**: Seamlessly integrates Poetry to build Python projects, handling dependency resolution and packaging within the AWS CDK framework.
- **Automated Deployment**: Automates the packaging and deployment process of Python Lambda functions, making deployments faster and more reliable.
- **Build Artifacts**: Generates build artifacts in a `dist/` directory adjacent to `pyproject.toml`, ensuring a structured and predictable build environment.


## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [AWS CDK](https://github.com/aws/aws-cdk)
- [Poetry](https://github.com/python-poetry/poetry)
- [poetry-plugin-export](https://github.com/python-poetry/poetry-plugin-export)

## Installation

To use PoetryAssetCode in your CDK project, install it via pip:

```bash
pip install cdk-poetry-asset-code
```

## Usage
Import `PoetryAssetCode` in your CDK stack and use it to define the code for your AWS Lambda function:
```python
from aws_cdk import Stack
from constructs import Construct
from aws_cdk.aws_lambda import Function, Runtime
from poetry_asset_code import PoetryAssetCode

class MyLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        lambda_function = Function(
            self, "MyPoetryLambdaFunction",
            runtime=Runtime.PYTHON_3_12,
            handler="handler.main",
            code=PoetryAssetCode("/path/to/your/poetry/project")
        )
```

## Configuration
PoetryAssetCode accepts the following parameters:

- `path`: Path to the directory containing the Poetry project (where pyproject.toml is located).
- Additional AWS CDK AssetCode parameters as needed.


## Local Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging, and it's recommended to use Poetry to run local development tasks to ensure consistency with the project's dependencies.

### Running tests
All the tests are based on [pytest](https://docs.pytest.org/) so running them boils down to executing one command:
```shell
poetry run pytest
```

### Running Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality and formatting standards. To set up pre-commit hooks within the Poetry environment, which ensures that the hooks are run automatically before each commit, execute the following command:

```bash
poetry run pre-commit install
```

This command installs pre-commit hooks as Git pre-commit hooks, so they are automatically executed before you commit changes. It's a convenient way to ensure your changes adhere to the project's standards without needing to manually run checks before each commit.

If you prefer to run pre-commit hooks manually, perhaps to check files before committing, you can use the following command:
```bash
poetry run pre-commit run --all-files
```
This will manually execute all configured pre-commit hooks on all files in the repository. It's useful for performing a one-time check or for scenarios where you haven't set up automatic pre-commit hooks with pre-commit install.


### Running Pyright
Pyright is used for static type checking to catch errors early in development. To run Pyright through Poetry, use the following command:

bash
```
poetry run pyright
```

This will execute Pyright type checking based on the project's pyrightconfig.json configuration. Running Pyright helps ensure type consistency and can catch common errors.


## Contributing
- Submitting bug reports and feature requests in the Issues section.
- Opening pull requests with improvements to code or documentation.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- Thanks to the AWS CDK team for providing the framework.
- Thanks to the Poetry team for simplifying Python package management.
