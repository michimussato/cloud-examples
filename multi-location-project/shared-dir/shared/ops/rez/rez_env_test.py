import os
import subprocess

from dagster import (
    Output,
    AssetMaterialization,
    MetadataValue,
    op,
    In,
    AssetExecutionContext,
)


@op(
    ins={
        "RND_PACKAGES": In(),
        "AL_PACKAGE_NAME": In(),
        "AL_PACKAGE_VERSION": In(),
        "REZ_EXE": In(),
        "AL_LAUNCHER_PRESET": In(),
        "overrides": In(),
        # Todo: "build_test_package": In(),
    },
)
def rez_env_test(
        context: AssetExecutionContext,
        RND_PACKAGES: str,
        AL_PACKAGE_NAME: str,
        AL_PACKAGE_VERSION: str,
        REZ_EXE: str,
        AL_LAUNCHER_PRESET: str,
        overrides: dict,
        # Todo: build_test_package: str,
) -> dict:
    """
    Testing if the path to test package
    is in PATH.

    ```
    Args:
        context ():
        RND_PACKAGES ():
        AL_PACKAGE_NAME ():
        AL_PACKAGE_VERSION ():
        REZ_EXE ():
        AL_LAUNCHER_PRESET ():
        overrides ():

    Returns:

    ```
    """

    overrides_ = []

    for override in overrides["prepends"]:
        if not bool(override):
            raise Exception("Overrides must not contain empty dicts.")
        var_name = override["var_name"]
        var_value = override["var_value"]
        overrides_.append(f"{var_name}={var_value}{os.pathsep}${var_name}")

    _overrides = ','.join(overrides_)

    pkg = f"{AL_PACKAGE_NAME}-{AL_PACKAGE_VERSION}"
    # AL_otio-3.9.7                                    /depts/rnd/dev/michaelmus/packages/AL_otio/3.9.7
    pkg_path = f"{os.sep.join([RND_PACKAGES, AL_PACKAGE_NAME, AL_PACKAGE_VERSION])}"

    _path = "__".join(context.asset_key.path)

    env_txt = f"/home/users/michaelmus/pycharm/tickets/PTP-432/dagster/PTP-432/PTP_432/out/{_path}_rez_context_{pkg}.txt"

    cmd = [
        REZ_EXE,
        'env',
        'launcher2CL',
        '-c',
        f'$LAUNCH_EXE -l shell -p {AL_LAUNCHER_PRESET} {"-D " + _overrides if bool(_overrides) else ""} -c \"rez context > {env_txt}\"']

    context.log.info(cmd)

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = proc.communicate()
    return_code = proc.returncode
    context.log.info(stdout)
    context.log.error(stderr)
    context.log.info(return_code)

    _pkg_in_env = False
    with open(env_txt, "r") as fr:
        for line in fr:
            if all(s in line for s in [pkg, pkg_path]):
                _pkg_in_env = True

    if not _pkg_in_env:
        raise Exception(f"{pkg} not found in test environment.")

    yield Output(_pkg_in_env)
    # yield Output(dict(os.environ), output_name="env_full")

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            'path to test package': MetadataValue.path(pkg_path),
            'resolve to test package': MetadataValue.bool(_pkg_in_env),
            'cmd': MetadataValue.json(cmd),
            'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
            'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
        }
    )
