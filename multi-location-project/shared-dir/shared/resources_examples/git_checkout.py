import pathlib

from shared.factories.asset_factory import asset_factory

from dagster import (
    AssetsDefinition,
    MetadataValue,
)


package: str = "AL_vortex_library_edit"
version: str = "0.33.2"
git_repo: str = "vortexLibrary"


package_dict: dict = {
    "package": package,
    "version": version,
    "git_repo": git_repo,
    "group_name": package,
    "assets": [
        {
            # The local folder where the package.py file of this package lives
            "name": "BUILD_CWD",
            "key_prefix": [package],
            "value": f"{pathlib.Path.home()}/pycharm/tickets/PTP-432/env/git/repos/animallogic-rnd/{git_repo}/src/AL/vortex/libraryedit",
            "type": MetadataValue.path,
            "deps": {},
        },
        {
            # The SSH Git Repo URL
            "name": "GIT_SSH",
            "key_prefix": [package],
            "value": f"git@github.com:animallogic-rnd/{git_repo}.git",
            "type": MetadataValue.path,
            "deps": {},
        },
        {
            "name": "GIT_REPO_NAME",
            "key_prefix": [package],
            "value": git_repo,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            # The name of the main branch
            "name": "MASTER_BRANCH",
            "key_prefix": [package],
            "value": "master",
            "type": MetadataValue.text,
            "deps": {},
        },
        # {
        #     # The link to th OPEN pull request
        #     "name": "AL_PACKAGE_PR",
        #     "key_prefix": package,
        #     "value": "https://github.com/animallogic-rnd/vortexLibrary/pull/1966",
        #     "type": MetadataValue.url,
        #     "deps": {},
        # },
        {
            # The package name as defined in the package.py (can be different
            # from repo name)
            "name": "AL_PACKAGE_NAME",
            "key_prefix": [package],
            "value": package,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            # The incremented package version (checkout +major/minor/patch)
            "name": "AL_PACKAGE_VERSION",
            "key_prefix": [package],
            "value": version,
            "type": MetadataValue.text,
            "deps": {},
        },
    ],
}


def get_git_assets() -> list[AssetsDefinition]:
    git_checkout_assets = [
        asset_factory(
            group_name=f"AL_GIT_CHECKOUT__{git_dict['group_name']}",
            spec=spec,
        ) for spec in git_dict["assets"]
    ]
    return git_checkout_assets


# Creates a group of individual assets for each dict inside the package_dict["assets"] list.
# Works similarly like @multi_asset but seems easier to control.
if __name__ == "__main__":
    get_git_assets()




"""
    # checkout_dev_branch
    vars()[f"checkout_branch__{asset_from_op['package']}"] = AssetsDefinition.from_op(
        checkout_dev_branch,
        group_name="02__checkout_branch",
        keys_by_input_name={
            "BRANCH_NAME": AssetKey("BRANCH_NAME"),
            "GIT_REPO_NAME": AssetKey(
                [asset_from_op['package'], "GIT_REPO_NAME"]
            ),
            "MASTER_BRANCH": AssetKey(
                [asset_from_op['package'], "MASTER_BRANCH"]
            ),
            "LOCAL_GIT_REPO_DIR": AssetKey("LOCAL_GIT_REPO_DIR"),
        },
        keys_by_output_name={
            "result": AssetKey(f"checkout_branch__{asset_from_op['package']}"),
        },
    )
"""