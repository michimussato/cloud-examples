import git

from dagster import (
    op,
    In,
    Output,
    AssetExecutionContext,
    AssetMaterialization,
    MetadataValue,
)


@op(
    ins={
        "BRANCH_NAME": In(),
        "AL_PACKAGE_NAME": In(),
        "GIT_SSH": In(),
    },
)
def check_branch_exists_on_remote(
        context: AssetExecutionContext,
        BRANCH_NAME: str,
        AL_PACKAGE_NAME: str,
        GIT_SSH: str,

) -> bool:
    """
    Make sure that the dev branch exists on the remote.
    `rez test` will fail if not pushed prior.
    """

    # git ls-remote --heads origin refs/heads/$WRANGLER_BRANCH_NAME
    # PTP-432_Editron-uses-working-range-instead-of-cut-range-data-to-display-edit-changes
    # git@github.com:animallogic-rnd/AL_otio.git
    # git ls-remote --exit-code --heads git@github.com:animallogic-rnd/AL_otio.git refs/heads/PTP-432_Editron-uses-working-range-instead-of-cut-range-data-to-display-edit-changes
    # git.Repo("~/pycharm/tickets/PTP-432/env/git/repos/animallogic-rnd/AL_otio").git.ls_remote()

    # g = git.cmd.Git()
    # g.ls_remote("--exit-code", "--heads", "git@github.com:animallogic-rnd/AL_otio.git", "refs/heads/PTP-432_Editron-uses-working-range-instead-of-cut-range-data-to-display-edit-change")

    g = git.cmd.Git()

    try:
        # Todo: this does not work for packages deeper in the tree yet
        _ret = g.ls_remote("--exit-code", "--heads", GIT_SSH, f"refs/heads/{BRANCH_NAME}")
        yield Output(True)

        yield AssetMaterialization(
            asset_key=context.asset_key,
            metadata={
                'branch exists on remote': MetadataValue.bool(True),
                'ls-remote': MetadataValue.md(f"```{_ret}```"),
                'url': MetadataValue.url(
                    f"https://github.com/animallogic-rnd/{AL_PACKAGE_NAME}/tree/{BRANCH_NAME}"),
            }
        )
    except git.exc.GitCommandError as e:
        context.log.exception(e)
        raise Exception(
            f"Branch {BRANCH_NAME} "
            f"does not exist on remote {GIT_SSH}."
        ) from e
