import os
import subprocess
import tempfile

from dagster import (
    MetadataValue,
    op,
    In,
    AssetExecutionContext,
    MaterializeResult,
)


@op(
    ins={
        "BUILD_CWD": In(),
        "REZ_EXE": In(),
        "REZ_TEST__REZ_LOCAL_PACKAGES_PATH": In(),
        "AL_PACKAGE_NAME": In(),
    },
    # out=
)
def rez_test(
        context: AssetExecutionContext,
        BUILD_CWD: str,
        REZ_EXE: str,
        REZ_TEST__REZ_LOCAL_PACKAGES_PATH: str,
        AL_PACKAGE_NAME: str,
) -> MaterializeResult:
    """
    Rez testing package.
    Needs to succeed prior to `rez unleash`
    cmd: `rez test` to temporary directory.

    ```
    Args:
        AL_PACKAGE_NAME ():
        REZ_TEST__REZ_LOCAL_PACKAGES_PATH ():
        context ():
        BUILD_CWD ():
        REZ_EXE ():

    Returns:

    ```
    """

    # works:
    # REZ_LOCAL_PACKAGES_PATH=/home/users/michaelmus/temp rez test --paths /home/users/michaelmus/temp:/film/tools/packages
    # "REZ_FILESYSTEM_CACHE_PACKAGES_PATH": "/film/tools/packages/cache"
    # "REZ_RELEASE_PACKAGES_PATH": "/film/tools/packages"

    with tempfile.TemporaryDirectory(prefix=f"{REZ_TEST__REZ_LOCAL_PACKAGES_PATH}__{AL_PACKAGE_NAME}__") as tmp_dir:

        my_env = {**os.environ, "REZ_LOCAL_PACKAGES_PATH": tmp_dir}

        context.log.info(f"rez test temp directory: {tmp_dir}")

        cmd = [
            REZ_EXE,
            "test",
            "--paths",
            os.pathsep.join([
                my_env["REZ_LOCAL_PACKAGES_PATH"],
                my_env["REZ_RELEASE_PACKAGES_PATH"],
            ]),
        ]

        proc = subprocess.Popen(
            args=cmd,
            cwd=BUILD_CWD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=my_env,
            text=True,
        )

        stdout, stderr = proc.communicate()
        return_code = proc.returncode

        context.log.info(stdout)
        context.log.error(stderr)
        context.log.info(return_code)

    # if "Test failed with exit code 1" in stdout or return_code:
    if return_code:
        raise Exception("Test failed")

    yield MaterializeResult(
        asset_key=context.asset_key,
        metadata={
            # 'Test successful': MetadataValue.bool(True),
            'cwd': MetadataValue.path(BUILD_CWD),
            'cmd': MetadataValue.md(f"`{cmd}`"),
            'cmd (str)': MetadataValue.path(" ".join(cmd)),
            'environ (full)': MetadataValue.json(dict(os.environ)),
            'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
            'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
        }
    )
