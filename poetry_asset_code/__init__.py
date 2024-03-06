import shutil
import subprocess
import zipfile

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from aws_cdk import AssetHashType
from aws_cdk import BundlingOptions
from aws_cdk import IgnoreMode
from aws_cdk import SymlinkFollowMode
from aws_cdk.aws_iam import IGrantable
from aws_cdk.aws_lambda import AssetCode


class PoetryAssetCode(AssetCode):
    """
    A custom AWS CDK AssetCode implementation that builds a Python Lambda function package using Poetry.

    This class automates the process of building a Poetry-based Python project, including resolving
    dependencies, packaging the project, and preparing it for deployment as an AWS Lambda function.
    Temporary build artifacts are generated in a `dist/` directory relative to the pyproject.toml.

    Prerequisites:
        - Poetry must be installed in the environment where the CDK app is executed.
          For installation instructions, refer to: https://python-poetry.org/docs/#installation
        - The `poetry-plugin-export` plugin is required for exporting the project's dependencies to a
          `requirements.txt` file, refer to: https://python-poetry.org/docs/plugins/

    Example:
        Below is an example of how to use the `PoetryAssetCode` within an AWS CDK Stack to define a Lambda function:

        ```python
        from aws_cdk import Stack
        from aws_cdk.aws_lambda import Function, Runtime
        from constructs import Construct
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
    """

    def __init__(
        self,
        path: str,
        *,
        deploy_time: bool | None = None,
        readers: Sequence[IGrantable] | None = None,
        asset_hash: str | None = None,
        asset_hash_type: AssetHashType | None = None,
        bundling: BundlingOptions | dict[str, Any] | None = None,
        exclude: Sequence[str] | None = None,
        follow_symlinks: SymlinkFollowMode | None = None,
        ignore_mode: IgnoreMode | None = None,
    ) -> None:
        """
        Args:
            :param path: A path to the directory where the pyproject.toml file resides.
            > Please see the parent class _init__ for information about other params.
        """
        src_path = Path(path)
        poetry_dist_path = src_path / "dist"
        output_path = poetry_dist_path / "lambda_output"

        self._prepare_directory(poetry_dist_path)
        self._build_local_code(src_path, poetry_dist_path, output_path)
        self._attach_third_parties(src_path, poetry_dist_path, output_path)

        super().__init__(
            str(output_path),
            deploy_time=deploy_time,
            readers=readers,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

    @staticmethod
    def _prepare_directory(path: Path) -> None:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir()

    @staticmethod
    def _build_local_code(src_path: Path, dist_path: Path, output_path: Path) -> None:
        subprocess.run(["poetry", "build", "-f", "wheel"], check=True, cwd=src_path)
        wheels = list(dist_path.glob("*.whl"))
        if not wheels:
            raise FileNotFoundError("No wheel file found in the dist directory.")
        wheel_path = wheels[0]

        with zipfile.ZipFile(wheel_path, "r") as zip_ref:
            zip_ref.extractall(output_path)

    @staticmethod
    def _attach_third_parties(
        src_path: Path, requirements_path: Path, output_path: Path
    ) -> None:
        requirements_txt = requirements_path / "requirements.txt"
        subprocess.run(
            [
                "poetry",
                "export",
                "-f",
                "requirements.txt",
                "--output",
                requirements_txt,
            ],
            check=True,
            cwd=src_path,
        )
        subprocess.run(
            ["pip", "install", "-r", requirements_txt, "-t", output_path], check=True
        )
