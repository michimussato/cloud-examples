from cowsay import main

from dagster import (Nothing,
                     # AssetExecutionContext,
                     # MetadataValue,
                     # AssetSpec,
                     # Output,
                     # AssetMaterialization,
                     # AssetIn,
                     # AssetOut,
                     asset,
                     AssetsDefinition,
                     # AssetIn,
                     AssetKey,
                     # OpExecutionContext,
                     # op,
                     # GraphDefinition,
                     # DependencyDefinition,
                     # multi_asset,
                     # MaterializeResult,
                     )

from shared import shared_function
from shared.ops.rez_test import rez_test
# from shared.factories.multi_asset.multi_asset_factory import multi_asset_factory
from shared.factories.asset.asset import asset_factory
from shared.ops.build_test_package import build_test_package


# Simple single asset
@asset
def BUILD_CWD(context) -> dict:
    context.log.info(shared_function())
    context.log.info(f"Cowsay version {main.__version__}")
    return Nothing
@asset
def REZ_EXE(context) -> dict:
    context.log.info(shared_function())
    context.log.info(f"Cowsay version {main.__version__}")
    return Nothing
@asset
def REZ_TEST__REZ_LOCAL_PACKAGES_PATH(context) -> dict:
    context.log.info(shared_function())
    context.log.info(f"Cowsay version {main.__version__}")
    return Nothing
@asset
def AL_PACKAGE_NAME(context) -> dict:
    context.log.info(shared_function())
    context.log.info(f"Cowsay version {main.__version__}")
    return Nothing


# Assets from re-usable ops
rez_test_1__from_op = AssetsDefinition.from_op(
    op_def=rez_test,
    key_prefix=[
        "rez_test_1",
    ],
    group_name="rez_test_1",
)

rez_test_2_from_op = AssetsDefinition.from_op(
    op_def=rez_test,
    key_prefix=[
        "rez_test_2",
        "sub_prefix",
    ],
    group_name="rez_test_2",
)

build_test_package_asset_from_op = AssetsDefinition.from_op(
    op_def=build_test_package,
    keys_by_input_name={
        # "BUILD_CWD": AssetKey("BUILD_CWD"),
        # "RND_PACKAGES": AssetKey("RND_PACKAGES"),
        # "AL_PACKAGE_NAME": AssetKey("AL_PACKAGE_NAME"),
        # "AL_PACKAGE_VERSION": AssetKey("AL_PACKAGE_VERSION"),
        "REZ_EXE": AssetKey("REZ_EXE"),
        # "black": AssetKey("black"),
    },
)


# assets from factory
packages = [
    {
        "package_name": "AL_otio",
        "package_version": "3.9.7",
        # "git_repo": "AL_otio",
        # "key_prefix": "AL_otio",
        # "deps": [],
    },
    {
        "package_name": "AL_vortex_library_edit",
        "package_version": "0.33.2",
        # "git_repo": "vortexLibrary",
        # "key_prefix": "AL_vortex_library_edit",
        # "deps": [],
    }
]


_packages = [asset_factory(package["package_name"], package) for package in packages]
