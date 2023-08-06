"""Module with functions for 'tests' subpackage."""

from __future__ import annotations
from typing import Sequence, cast
from pathlib import Path
import sys
import warnings
import os
import platform

from typing_extensions import Literal
import numpy as np
import mylogging

from mypythontools.paths import validate_path, PathLike
from mypythontools.system import (
    get_console_str_with_quotes,
    terminal_do_command,
    check_library_is_available,
    is_wsl,
)
from mypythontools.misc import delete_files
from mypythontools.config import Config, MyProperty

from ..venvs import Venv
from mypythontools_cicd.project_paths import PROJECT_PATHS


class TestConfig(Config):
    """Allow to setup tests."""

    @MyProperty
    @staticmethod
    def tested_path() -> None | PathLike:
        """Define path of tested folder.

        Type:
            None | PathLike

        Default:
            None

        If None, root is used. Root is necessary if using doctest, 'tests' folder not works for doctest.
        """
        return None

    @MyProperty
    @staticmethod
    def run_tests() -> bool:
        """Define whether run tests or not.

        Type:
            bool

        Default:
            True
        """
        return True

    @MyProperty
    @staticmethod
    def tests_path() -> None | PathLike:
        """If None, tests is used. It means where venv will be stored etc.

        Type:
            None | PathLike

        Default:
            None
        """
        return None

    @MyProperty
    @staticmethod
    def test_coverage() -> bool:
        """Whether run test coverage plugin. If True, pytest-cov must be installed.

        Type:
            bool

        Default:
            True
        """
        return True

    @MyProperty
    @staticmethod
    def stop_on_first_error() -> bool:
        """Whether stop on first error.

        Type:
            bool

        Default:
            True
        """
        return True

    @MyProperty
    @staticmethod
    def virtualenvs() -> None | Sequence[PathLike]:
        """Virtualenvs used to testing. It's used to be able to test more python versions at once.

        Example:
            ``["venv/3.7", "venv/3.10"]``. If you want to use current venv, use `sys.prefix`. If there is no
            venv, it's created with default virtualenv version.

        Type:
            None | Sequence[PathLike]

        Default:
            ["venv/3.7", "venv/3.10"]

        If no `virtualenvs` nor `wsl_virtualenvs` is configured, then default python will be used.
        """
        return ["venv/3.7", "venv/3.10"]

    @MyProperty
    @staticmethod
    def wsl_virtualenvs() -> None | Sequence[PathLike]:
        """Define which wsl virtual environments will be tested.

        Type:
            None | Sequence[PathLike]

        Default:
            ["venv/wsl-3.7", "venv/wsl-3.7"]
        """
        return ["venv/wsl-3.7", "venv/wsl-3.7"]

    @MyProperty
    @staticmethod
    def sync_requirements() -> None | Literal["infer"] | PathLike | Sequence[PathLike]:
        """Define whether update libraries versions.

        Type:
            None | Literal["infer"] | PathLike | Sequence[PathLike]

        Default:
            "infer"

        If using `virtualenvs` define what libraries will be installed by path to requirements.txt. Can
        also be a list of more files e.g ``["requirements.txt", "requirements_dev.txt"]``. If "infer",
        auto detected (all requirements).
        """
        return "infer"

    @MyProperty
    @staticmethod
    def verbosity() -> Literal[0, 1, 2]:
        """Define whether print details on errors or keep silent.

        Type:
            Literal[0, 1, 2]

        Default:
            1

        If 0, no details, parameters `-q and `--tb=line` are added. if 1, some details are added --tb=short.
        If 2, more details are printed (default --tb=auto).
        """
        return 1

    @MyProperty
    @staticmethod
    def extra_args() -> None | list:
        """List of args passed to pytest.

        Type:
            None | list

        Default:
            None
        """
        return None


default_test_config = TestConfig()


def run_tests(
    config: TestConfig = default_test_config,
) -> None:
    """Run tests. If any test fails, raise an error.

    This is not supposed for normal testing during development. It's usually part of pipeline an runs just
    before pushing code. It usually runs on more python versions and it's syncing dependencies, so takes much
    more time than testing in IDE.

    Args:
        config (PipelineConfig, optional): TestConfig configuration object. Just import default_test_config
            and use intellisense and help tooltip with description. Defaults to `default_test_config`.

    Raises:
        Exception: If any test fail, it will raise exception (git hook do not continue...).

    Note:
        By default args to quiet mode and no traceback are passed. Usually this just runs automatic tests.
        If some of them fail, it's further analyzed in some other tool in IDE.

    Example:
        ``run_tests(verbosity=2)``
    """
    if not config.run_tests:
        return

    tested_path = validate_path(config.tested_path) if config.tested_path else PROJECT_PATHS.root
    tests_path = validate_path(config.tests_path) if config.tests_path else PROJECT_PATHS.tests
    tested_path_str = get_console_str_with_quotes(tested_path)

    verbosity = config.verbosity
    verbose = True if verbosity == 2 else False

    # If using wsl, use recursion, call function itself with prepended wsl and
    # changing corresponding `virtualenvs` config
    # This will be skipped when running on wsl as `wsl_virtualenvs` is emptied
    if config.wsl_virtualenvs:
        if platform.system() == "Windows" and not is_wsl():
            wsl_virtualenvs = (
                [config.wsl_virtualenvs]
                if isinstance(config.wsl_virtualenvs, (str, Path))
                else config.wsl_virtualenvs
            )

            for i in wsl_virtualenvs:
                if verbosity:
                    print(f"\tPreparing wsl environment {i}.")

                wsl_config = config.copy()

                wsl_config.virtualenvs = [i]

                if not Path(i).exists():
                    raise RuntimeError("Venv doesn't exists. Create it first with 'venvs.prepare_venvs()'")
                terminal_do_command(
                    f"wsl {i}/bin/python -m pip install mypythontools_cicd",
                    verbose=verbose,
                    error_header=f"Installing pytest to wsl venv {i} failed.",
                )

                test_config = " ".join(
                    f"--{i} {j}"
                    for i, j in wsl_config.get_dict().items()
                    if i not in ["virtualenvs", "wsl_virtualenvs"]
                )

                terminal_do_command(
                    f'wsl {i}/bin/python -m mypythontools_cicd --do_only test {test_config}"',
                    cwd=tested_path.as_posix(),
                    verbose=verbose,
                    error_header="Tests failed.",
                )

    if not config.virtualenvs:
        return

    extra_args = config.extra_args if config.extra_args else []

    if config.stop_on_first_error:
        extra_args.append("-x")

    if verbosity == 0:
        extra_args.append("-q")
        extra_args.append("--tb=line")
    elif verbosity == 1:
        extra_args.append("--tb=short")

    complete_args = (
        "pytest",
        tested_path_str,
        *extra_args,
    )

    test_command = " ".join(complete_args)

    sync_requirements = config.sync_requirements
    if (
        sync_requirements
        and sync_requirements != "infer"
        and isinstance(sync_requirements, (Path, str, os.PathLike))
    ):
        sync_requirements = [sync_requirements]
    sync_requirements = cast(list, sync_requirements)

    virtualenvs = config.virtualenvs

    if virtualenvs:
        test_commands: list[str] = []
        virtualenvs = [virtualenvs] if isinstance(virtualenvs, (str, Path)) else virtualenvs
        for i in virtualenvs:
            my_venv = Venv(i)
            if not my_venv.installed:
                raise RuntimeError(
                    "Defined virtualenv not found. Use 'venvs.prepare_venvs' or install venvs manually."
                )

            if sync_requirements:
                if verbosity:
                    print(f"\tSyncing requirements in venv '{my_venv.venv_path.name}' for tests")
                my_venv.sync_requirements(sync_requirements, verbose)
            # To be able to not install dev requirements in older python venv, pytest is installed.
            # Usually just respond with Requirements already satisfied.
            my_venv.install_library("pytest")
            test_commands.append(f"{my_venv.activate_command} && {test_command}")
    else:
        test_commands: list[str] = [test_command]

    if config.test_coverage:
        # Add coverage only to first virtualenv
        xml_path = f"xml:{tests_path / 'coverage.xml'}"
        cov_str = (
            f" --cov {get_console_str_with_quotes(PROJECT_PATHS.app)} --cov-report "
            f"{get_console_str_with_quotes(xml_path)}"
        )

        test_commands[0] = test_commands[0] + cov_str
    for i, command in enumerate(test_commands):
        if verbosity and virtualenvs:
            print(f"\tStarting tests with venv `{virtualenvs[i]}`")

        terminal_do_command(
            command, cwd=tested_path.as_posix(), verbose=verbose, error_header="Tests failed."
        )

    if config.test_coverage:
        delete_files(".coverage")


def setup_tests(
    generate_readme_tests: bool = True,
    matplotlib_test_backend: bool = False,
    set_numpy_random_seed: int | None = 2,
) -> None:
    """Add paths to be able to import local version of library as well as other test files.

    Value Mylogging.config.colorize = 0 changed globally.

    Note:
        Function expect `tests` folder on root. If not, test folder will not be added to sys path and
        imports from tests will not work.

    Args:
        generate_readme_tests (bool, optional): If True, generate new tests from readme if there are
            new changes. Defaults to True.
        matplotlib_test_backend (bool, optional): If using matlplotlib, it need to be
            closed to continue tests. Change backend to agg. Defaults to False.
        set_numpy_random_seed (int | None): If using numpy random numbers, it will be each time the same.
            Defaults to 2.

    """
    mylogging.config.colorize = False

    PROJECT_PATHS.add_root_to_sys_path()

    # Find paths and add to sys.path to be able to import local modules
    test_dir_path = PROJECT_PATHS.tests

    if test_dir_path.as_posix() not in sys.path:
        sys.path.insert(0, test_dir_path.as_posix())

    if matplotlib_test_backend:
        check_library_is_available("matplotlib")
        import matplotlib

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            matplotlib.use("agg")

    if generate_readme_tests:
        add_readme_tests()

    if set_numpy_random_seed:
        np.random.seed(2)


def add_readme_tests(readme_path: None | PathLike = None, test_folder_path: None | PathLike = None) -> None:
    """Generate pytest tests script file from README.md and save it to tests folder.

    Can be called from conftest.

    Args:
        readme_path (None | PathLike, optional): If None, autodetected (README.md, Readme.md or readme.md
            on root). Defaults to None.
        test_folder_path (None | PathLike, optional): If None, autodetected (if root / tests).
            Defaults to None.

    Raises:
        FileNotFoundError: If Readme not found.

    Example:
        >>> add_readme_tests()

        Readme tests found.

    Note:
        Only blocks with python defined syntax will be evaluated. Example::

            ```python
            import numpy
            ```

        If you want to import modules and use some global variables, add ``<!--phmdoctest-setup-->`` directive
        before block with setup code.
        If you want to skip some test, add ``<!--phmdoctest-mark.skip-->``
    """
    readme_path = validate_path(readme_path) if readme_path else PROJECT_PATHS.readme
    test_folder_path = validate_path(test_folder_path) if test_folder_path else PROJECT_PATHS.tests

    readme_date_modified = str(readme_path.stat().st_mtime).split(".", maxsplit=1)[0]  # Keep only seconds
    readme_tests_name = f"test_readme_generated-{readme_date_modified}.py"

    test_file_path = test_folder_path / readme_tests_name

    # File not changed from last tests
    if test_file_path.exists():
        return

    for i in test_folder_path.glob("*"):
        if i.name.startswith("test_readme_generated"):
            i.unlink()

    python_path = get_console_str_with_quotes(sys.executable)
    readme = get_console_str_with_quotes(readme_path)
    output = get_console_str_with_quotes(test_file_path)

    generate_readme_test_command = f"{python_path} -m phmdoctest {readme} --outfile {output}"

    terminal_do_command(generate_readme_test_command, error_header="Readme test creation failed")


def deactivate_test_settings() -> None:
    """Deactivate functionality from setup_tests.

    Sometimes you want to run test just in normal mode (enable plots etc.). Usually at the end of
    test file in ``if __name__ = "__main__":`` block.
    """
    mylogging.config.colorize = True

    if "matplotlib" in sys.modules:

        import matplotlib
        from importlib import reload

        reload(matplotlib)
