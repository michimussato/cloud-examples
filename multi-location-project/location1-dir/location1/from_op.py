from dagster import (AssetsDefinition,
                     AssetKey,
                     )

from .packages.affected_package_1 import package_dict as package_dict_affected_package_1
from .packages.affected_package_2 import package_dict as package_dict_affected_package_2
from shared.resources_examples.package_definition import package_dict
from shared.ops.build_test_package import build_test_package
from shared.ops.git.checkout import checkout


for asset_from_op in [package_dict, package_dict_affected_package_1, package_dict_affected_package_2]:
    # build_test_package
    # dynamically creating variables for AssetsDefinition.from_op()
    # important thing is that the variable name is unique across
    # the code location
    vars()[f"build_test_package_{asset_from_op['package']}"] = AssetsDefinition.from_op(
        build_test_package,
        group_name="build_test_packages",
        # keys_by_input_name={
        #     "BUILD_CWD": AssetKey(
        #         [asset_from_op['package'], "BUILD_CWD"],
        #     ),
        #     "RND_PACKAGES": AssetKey("RND_PACKAGES"),
        #     "AL_PACKAGE_NAME": AssetKey(
        #         [asset_from_op['package'], "AL_PACKAGE_NAME"],
        #     ),
        #     "AL_PACKAGE_VERSION": AssetKey(
        #         [asset_from_op['package'], "AL_PACKAGE_VERSION"],
        #     ),
        #     "REZ_EXE": AssetKey("REZ_EXE"),
        #     "black": AssetKey(f"black_formatter__{asset_from_op['package']}"),
        # },
        keys_by_output_name={
            "result": AssetKey(f"build_test_package_{asset_from_op['package']}"),
        },
    )
    vars()[f"checkout_{asset_from_op['package']}"] = AssetsDefinition.from_op(
        checkout,
        group_name="checkout",
        # keys_by_input_name={
        #     "BUILD_CWD": AssetKey(
        #         [asset_from_op['package'], "BUILD_CWD"],
        #     ),
        #     "RND_PACKAGES": AssetKey("RND_PACKAGES"),
        #     "AL_PACKAGE_NAME": AssetKey(
        #         [asset_from_op['package'], "AL_PACKAGE_NAME"],
        #     ),
        #     "AL_PACKAGE_VERSION": AssetKey(
        #         [asset_from_op['package'], "AL_PACKAGE_VERSION"],
        #     ),
        #     "REZ_EXE": AssetKey("REZ_EXE"),
        #     "black": AssetKey(f"black_formatter__{asset_from_op['package']}"),
        # },
        keys_by_output_name={
            "result": AssetKey(f"checkout_{asset_from_op['package']}"),
        },
    )
