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


# @op(
#     ins={
#         # "BRANCH_NAME": In(),
#         "GIT_REPO_NAME": In(),
#         "MASTER_BRANCH": In(),
#         "LOCAL_GIT_REPO_DIR": In(),
#     },
# )
# def checkout_main_branch(
#         context: AssetExecutionContext,
#         # BRANCH_NAME: str,
#         GIT_REPO_NAME: str,
#         MASTER_BRANCH: str,
#         LOCAL_GIT_REPO_DIR: str,
#
# ) -> MaterializeResult:
#     """
#     Check out main (or master) branch.
#     """
#
#     repo = git.Repo(os.path.join(LOCAL_GIT_REPO_DIR, GIT_REPO_NAME))
#
#     # try:
#     result = repo.git.checkout(MASTER_BRANCH)
#     #     # push = repo.git.push("--set-upstream", repo.remote().name, BRANCH_NAME)
#     # except GitCommandError as checkout_err:
#     #     context.log.warning(checkout_err)
#     #     result = repo.git.checkout(BRANCH_NAME)
#     #     # push = None
#     # finally:
#     #     try:
#     #         push = repo.git.push("--set-upstream", repo.remote().name, BRANCH_NAME)
#     #     except GitCommandError as push_err:
#     #         push = "Maybe branch already exists on remote"
#     #         # raise Exception("Maybe branch already exists on remote?") from push_err
#     #         context.log.warning(f"{push}:\n{push_err}")
#
#     yield MaterializeResult(
#         asset_key=context.asset_key,
#         metadata={
#             'Result': MetadataValue.json(result),
#             # 'Push': MetadataValue.json(push),
#         }
#     )


@op(
    ins={
        "BRANCH_NAME": In(),
        "GIT_REPO_NAME": In(),
        "MASTER_BRANCH": In(),
        "LOCAL_GIT_REPO_DIR": In(),
    },
)
def checkout_dev_branch(
        context: AssetExecutionContext,
        BRANCH_NAME: str,
        GIT_REPO_NAME: str,
        MASTER_BRANCH: str,
        LOCAL_GIT_REPO_DIR: str,

) -> MaterializeResult:
    """
    Checkout dev branch.
    """

    repo = git.Repo(os.path.join(LOCAL_GIT_REPO_DIR, GIT_REPO_NAME))

    try:
        # -b means create (if it does not exist) and
        # checkout BRANCH_NAME
        # Todo
        #  test with
        #  repo.create_head(BRANCH_NAME)
        result = repo.git.checkout(MASTER_BRANCH, b=BRANCH_NAME)
        # push = repo.git.push("--set-upstream", repo.remote().name, BRANCH_NAME)
    except GitCommandError as checkout_err:
        context.log.warning(checkout_err)
        result = repo.git.checkout(BRANCH_NAME)
        # push = None
    finally:
        try:
            push = repo.git.push("--set-upstream", repo.remote().name, BRANCH_NAME)
        except GitCommandError as push_err:
            push = "Maybe branch already exists on remote"
            # raise Exception("Maybe branch already exists on remote?") from push_err
            context.log.warning(f"{push}:\n{push_err}")

    yield MaterializeResult(
        asset_key=context.asset_key,
        metadata={
            'Result': MetadataValue.json(result),
            'Push': MetadataValue.json(push),
        }
    )
