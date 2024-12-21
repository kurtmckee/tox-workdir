from __future__ import annotations

import pathlib
import typing
import uuid

import pytest
import tox.pytest

commands = pytest.mark.parametrize("command", ("workdir", "wd"))


@commands
def test_workdir_default(
    command: str,
    tox_project: typing.Callable[[dict[str, str]], tox.pytest.ToxProject],
) -> None:
    result = tox_project({}).run(command)
    result.assert_success()

    # The final line must be a path.
    assert result.out != ""
    workdir_path = pathlib.Path(result.out.split()[-1])

    # The final directory name must be an MD5 hash.
    assert len(workdir_path.name) == 32
    assert set(workdir_path.name).issubset(set("0123456789abcdef"))

    # As a sanity check, `.tox/` must not appear in the path.
    assert ".tox" not in str(workdir_path)


@commands
def test_workdir_option_override(
    command: str,
    tox_project: typing.Callable[[dict[str, str]], tox.pytest.ToxProject],
) -> None:
    unique_id = str(uuid.uuid4())

    result = tox_project({}).run(command, "--workdir", unique_id)
    result.assert_success()

    # The final line must be a path.
    assert result.out != ""
    workdir_path = pathlib.Path(result.out.split()[-1])

    # The final directory name must be the unique hash generated above.
    assert workdir_path.name == unique_id

    # As a sanity check, `.tox/` must not appear in the path.
    assert ".tox" not in str(workdir_path)


@commands
def test_workdir_config_override(
    command: str,
    tox_project: typing.Callable[[dict[str, str]], tox.pytest.ToxProject],
) -> None:
    unique_id = str(uuid.uuid4())

    result = tox_project({"tox.ini": f"[tox]\nwork_dir = {unique_id}"}).run(command)
    result.assert_success()

    # The final line must be a path.
    assert result.out != ""
    workdir_path = pathlib.Path(result.out.split()[-1])

    # The final directory name must be the unique hash generated above.
    assert workdir_path.name == unique_id

    # As a sanity check, `.tox/` must not appear in the path.
    assert ".tox" not in str(workdir_path)
