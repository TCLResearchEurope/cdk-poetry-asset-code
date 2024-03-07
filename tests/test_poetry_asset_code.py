from pathlib import Path

import pytest

from poetry_asset_code import PoetryAssetCode


@pytest.fixture
def poetry_project_dir(tmp_path: Path) -> Path:
    path = tmp_path / "project"
    path.mkdir()
    return path


@pytest.fixture
def artifacts_dir(poetry_project_dir: Path) -> Path:
    return poetry_project_dir / "dist"


@pytest.fixture
def expected_output_dir(artifacts_dir: Path) -> Path:
    return artifacts_dir / "lambda_output"


@pytest.fixture(autouse=True)
def prepare_source_code(poetry_project_dir: Path) -> None:
    template_path = Path(__file__).parent / "resources" / "pyproject_template.toml"

    pyproject_content = template_path.read_text()
    (poetry_project_dir / "pyproject.toml").write_text(pyproject_content)
    (poetry_project_dir / "my_package").mkdir()
    (poetry_project_dir / "my_package" / "__init__.py").touch()


def test_make_a_fresh_build(
    poetry_project_dir: Path, expected_output_dir: Path
) -> None:
    PoetryAssetCode(str(poetry_project_dir))

    assert expected_output_dir.exists()
    assert any(expected_output_dir.iterdir())


def test_remove_old_artifacts_when_building(
    poetry_project_dir: Path, artifacts_dir: Path
) -> None:
    artifacts_dir.mkdir()
    old_content = artifacts_dir / "old_content.txt"
    old_content.write_text("This is old content")

    PoetryAssetCode(str(poetry_project_dir))

    assert not old_content.exists()


def test_copy_local_files(poetry_project_dir: Path, expected_output_dir: Path) -> None:
    PoetryAssetCode(str(poetry_project_dir))

    output_file = expected_output_dir / "my_package" / "__init__.py"
    assert (output_file).exists()


def test_copy_third_parties(
    poetry_project_dir: Path, expected_output_dir: Path
) -> None:
    PoetryAssetCode(str(poetry_project_dir))

    assert any(expected_output_dir.glob("requests*"))


def test_initialize_base_asset_code_with_correct_path(
    poetry_project_dir: Path, expected_output_dir: Path
) -> None:
    pac = PoetryAssetCode(str(poetry_project_dir))

    assert pac.path == str(expected_output_dir)
