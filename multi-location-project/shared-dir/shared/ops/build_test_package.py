import os
import subprocess

from dagster import (op,
                     In,
                     OpExecutionContext,
                     Output,
                     AssetMaterialization,
                     MetadataValue,
                     )


@op(
    ins={
        # "BUILD_CWD": In(),
        # "RND_PACKAGES": In(),
        # "AL_PACKAGE_NAME": In(),
        # "AL_PACKAGE_VERSION": In(),
        "REZ_EXE": In(),
        # "black": In(),
    },
)
def build_test_package(
        context: OpExecutionContext,
        # BUILD_CWD: str,
        # RND_PACKAGES: str,
        # AL_PACKAGE_NAME: str,
        # AL_PACKAGE_VERSION: str,
        # REZ_EXE: str,
        # black: bool,  # DEPENDENCY; not actually used
        **kwargs,
) -> str:
    """
    Building the test package to RND_PACKAGES.
    alias: `bre`
    cmd: `rez build -c -i --ba ' -Dsymlink=OFF' --prefix RND_PACKAGES`

    ```
    Args:
        context: OpExecutionContext
        BUILD_CWD:
        RND_PACKAGES:
        AL_PACKAGE_NAME:
        AL_PACKAGE_VERSION:
        REZ_EXE:
        black: DEPENDENCY; not actually used

    Returns:

    ```
    """

    # sending an argument in the style of '--ba " -Key=Value"'
    # is causing Popen with shell=False to fail!
    # forwarding args like that is very wonky

    # " -Dsymlink=OFF" is needed if package needs to be
    # picked up by farm or remote user.
    # if only testing locally:
    # `rez build -c -i  --prefix {RND_PACKAGES}` would
    # be sufficient
    cmd = f'{kwargs.get("REZ_EXE")} build -c -i --ba " -Dsymlink=OFF" --prefix {kwargs.get("RND_PACKAGES")}'

    proc = subprocess.Popen(
        args=cmd,
        cwd=kwargs.get("BUILD_CWD"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )

    stdout, stderr = proc.communicate()
    return_code = proc.returncode

    context.log.info(stdout)
    context.log.error(stderr)
    context.log.info(return_code)

    yield Output(os.sep.join([kwargs.get("RND_PACKAGES"), kwargs.get("AL_PACKAGE_NAME"), kwargs.get("AL_PACKAGE_VERSION")]))

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            'cmd': MetadataValue.path(cmd),
            # 'cmd (str)': MetadataValue.path(" ".join(cmd)),
            # 'environ (modifications)': MetadataValue.json(al_rnd_packages),
            'environ (full)': MetadataValue.json(dict(os.environ)),
            'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
            'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
            # 'returncode': MetadataValue.json(return_code),
        }
    )


# Example:
# build_test_package_AL_otio = AssetsDefinition.from_op(
#     build_test_package,
#     group_name="build_test_packages",
#     keys_by_input_name={
#         "BUILD_CWD": AssetKey(
#             ["AL_otio", "BUILD_CWD"],
#         ),
#         "RND_PACKAGES": AssetKey("RND_PACKAGES"),
#         "AL_PACKAGE_NAME": AssetKey(
#             ["AL_otio", "AL_PACKAGE_NAME"],
#         ),
#         "AL_PACKAGE_VERSION": AssetKey(
#             ["AL_otio", "AL_PACKAGE_VERSION"],
#         ),
#         "REZ_EXE": AssetKey("REZ_EXE"),
#         "black": AssetKey("black_AL_otio"),
#     },
#     keys_by_output_name={
#         "result": AssetKey("build_test_package_AL_otio"),
#     },
# )
