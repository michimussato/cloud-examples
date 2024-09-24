import os

import git
from git.exc import GitCommandError

from dagster import (
    op,
    In,
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue,
)


@op(
    ins={
        "GIT_SSH": In(),
        "LOCAL_GIT_REPO_DIR": In(),
        "GIT_REPO_NAME": In(),
    },
)
def clone_repo(
        context: AssetExecutionContext,
        GIT_SSH: str,
        LOCAL_GIT_REPO_DIR: str,
        GIT_REPO_NAME: str,

) -> MaterializeResult:
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

    local_git_folder = os.path.join(LOCAL_GIT_REPO_DIR, GIT_REPO_NAME)
    pre_exists = False

    try:
        git.Repo.clone_from(
            url=GIT_SSH,
            to_path=local_git_folder,
        )
    except GitCommandError:
        context.log.warning(f"Local Git repo already extists: {local_git_folder}")
        pre_exists = True

    yield MaterializeResult(
        asset_key=context.asset_key,
        metadata={
            'Local Repo': MetadataValue.path(local_git_folder),
            'Pre Existed': MetadataValue.bool(pre_exists),
        }
    )
