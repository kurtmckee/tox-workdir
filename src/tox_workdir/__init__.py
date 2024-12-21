import hashlib
import pathlib

import platformdirs
import tox.config.cli.parser
import tox.config.sets
import tox.plugin
import tox.session.state


@tox.plugin.impl
def tox_add_option(parser: tox.config.cli.parser.ToxParser) -> None:
    """Add a `workdir` (`wd`) command to tox."""

    parser.add_command("workdir", ["wd"], "show the base workdir", show_work_dir)


@tox.plugin.impl
def tox_add_core_config(
    core_conf: tox.config.sets.ConfigSet,
    state: tox.session.state.State,
) -> None:
    """Put the work directory in the user cache directory by default."""

    work_dir = get_work_dir(state)
    core_conf.add_config(
        "work_dir",
        of_type=pathlib.Path,
        default=work_dir,
        desc="work_dir default customized by tox-workdir plugin",
    )


def show_work_dir(state: tox.session.state.State) -> int:
    print(get_work_dir(state))
    return 0


def get_work_dir(
    state: tox.session.state.State,
) -> pathlib.Path:
    """Calculate the `work_dir` path."""

    # Honor the `--workdir` argument if it was passed.
    workdir_option: pathlib.Path | None = state.conf.options.work_dir
    if workdir_option is not None:
        return workdir_option.absolute().resolve()

    # Honor non-default `work_dir` configurations.
    workdir_config: pathlib.Path | None = state.conf.core["work_dir"]
    if workdir_config is not None and workdir_config.name != ".tox":
        return workdir_config.absolute().resolve()

    base_dir = platformdirs.user_cache_path(
        appauthor="kurtmckee",
        appname="tox-workdir",
    )
    md5_checksum = hashlib.md5(str(state.conf.src_path).encode("utf-8"))
    return base_dir / md5_checksum.hexdigest().lower()
