import os
import pathlib
import subprocess
import tempfile

import git

from dagster import (In,
                     MetadataValue,
                     AssetExecutionContext,
                     MaterializeResult,
                     op,
                     )


@op(
    ins={
        "BUILD_CWD": In(),
        "MASTER_BRANCH": In(),
        "BRANCH_NAME": In(),
        "LOCAL_GIT_REPO_DIR": In(),
        "GIT_REPO_NAME": In(),
        "REZ_EXE": In(),
        "REZ_UNLEASH__REZ_LOCAL_CLONE_PATH": In(),
        "AL_PACKAGE_NAME": In(),
        "GIT_SSH": In(),
        # "JIRA_TICKET": In(),
    },
)
def rez_unleash(
        context: AssetExecutionContext,
        BUILD_CWD: str,
        MASTER_BRANCH: str,
        BRANCH_NAME: str,
        LOCAL_GIT_REPO_DIR: str,
        GIT_REPO_NAME: str,
        REZ_EXE: str,
        REZ_UNLEASH__REZ_LOCAL_CLONE_PATH: str,
        AL_PACKAGE_NAME: str,
        GIT_SSH: str,
        # JIRA_TICKET: str,
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

    with tempfile.TemporaryDirectory(prefix=f"{REZ_UNLEASH__REZ_LOCAL_CLONE_PATH}__{AL_PACKAGE_NAME}__") as tmp_dir:

        context.log.info(f"Cloning {GIT_SSH} into {tmp_dir} from branch {BRANCH_NAME}...")

        # clone repo into temp dir
        repo = git.Repo.clone_from(
            url=GIT_SSH,
            to_path=tmp_dir,
            branch=BRANCH_NAME,
        )

        context.log.info(f"Checking out: {MASTER_BRANCH}")
        repo.git.checkout(MASTER_BRANCH)

        # # Merge BRANCH_NAME into MASTER_BRANCH
        merge_msg = "Test"
        # merge_msg = repo.git.merge(branch)
        context.log.info(f"Merge: {merge_msg}")
        #
        push_msg = "Test"
        # push_msg = repo.git.push()
        context.log.info(f"Push: {push_msg}")



        # # # # checkout master/main
        # # repo = git.Repo(os.path.join(LOCAL_GIT_REPO_DIR, GIT_REPO_NAME))
        # # context.log.info(f"Repo directory: {repo.git_dir = }")
        # # # Pull
        # pull = repo.remotes.origin.pull()

        # for remote in pull:
        #     context.log.info(f"Remote: {remote.name}")

        # main = getattr(repo.heads, MASTER_BRANCH)
        # context.log.info(f"Main: {main}")
        # branch = getattr(repo.heads, f"{BRANCH_NAME}")
        # context.log.info(f"Branch: {branch}")



        # main = getattr(repo.heads, MASTER_BRANCH)
        # context.log.info(f"Main: {main}")
        # branch = getattr(repo.heads, f"origin/{BRANCH_NAME}")
        # context.log.info(f"Branch: {branch}")

        # Checkout MASTER_BRANCH
        # checkout_main_msg = repo.git.checkout(main)
        # context.log.info(f"Checkout: {checkout_main_msg}")

        # # Merge BRANCH_NAME into MASTER_BRANCH
        # merge_msg = repo.git.merge(branch)
        # context.log.info(f"Merge: {merge_msg}")
        #
        # push_msg = repo.git.push()
        # context.log.info(f"Push: {push_msg}")

        # Todo
        #  Hardcoded here:
        unleash_msg_md = "/home/users/michaelmus/pycharm/tickets/PTP-432/dagster/PTP-432/PTP_432/rez/unleash_message.md"

        unleash_msg = str(pathlib.Path(unleash_msg_md).read_text(encoding="utf-8"))

        cmd = [
            REZ_EXE,
            "unleash",
            "--message",
            f"'{unleash_msg}'"
        ]

        context.log.info(cmd)

        proc = subprocess.Popen(
            args=cmd,
            cwd=BUILD_CWD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = proc.communicate()
        return_code = proc.returncode

        context.log.info(stdout)
        context.log.error(stderr)
        context.log.info(return_code)

        # # Checkout FEATURE
        # checkout_branch_msg = repo.git.checkout(branch)
        # context.log.info(f"Checkout: {checkout_branch_msg}")

    # if "Test failed with exit code 1" in stdout or return_code:
    # if return_code:
    #     raise Exception("rez unleash failed")

    yield MaterializeResult(
        asset_key=context.asset_key,
        metadata={
            # 'Test successful': MetadataValue.bool(True),
            'cwd': MetadataValue.path(BUILD_CWD),
            'cmd': MetadataValue.md(f"`{cmd}`"),
            'cmd (str)': MetadataValue.path(" ".join(cmd)),
            'environ (full)': MetadataValue.json(dict(os.environ)),
            # 'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
            # 'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
        }
    )@op(
    ins={
        "BUILD_CWD": In(),
        "MASTER_BRANCH": In(),
        "BRANCH_NAME": In(),
        "LOCAL_GIT_REPO_DIR": In(),
        "GIT_REPO_NAME": In(),
        "REZ_EXE": In(),
        "REZ_UNLEASH__REZ_LOCAL_CLONE_PATH": In(),
        "AL_PACKAGE_NAME": In(),
        "GIT_SSH": In(),
        # "JIRA_TICKET": In(),
    },
)
def rez_unleash_test(
        context: AssetExecutionContext,
        BUILD_CWD: str,
        MASTER_BRANCH: str,
        BRANCH_NAME: str,
        LOCAL_GIT_REPO_DIR: str,
        GIT_REPO_NAME: str,
        REZ_EXE: str,
        REZ_UNLEASH__REZ_LOCAL_CLONE_PATH: str,
        AL_PACKAGE_NAME: str,
        GIT_SSH: str,
        # JIRA_TICKET: str,
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

    with tempfile.TemporaryDirectory(prefix=f"{REZ_UNLEASH__REZ_LOCAL_CLONE_PATH}__{AL_PACKAGE_NAME}__") as tmp_dir:

        context.log.info(f"Cloning {GIT_SSH} into {tmp_dir} from branch {BRANCH_NAME}...")

        cmd = [
            REZ_EXE,
            "unleash",
            "--message",
            f"'{unleash_msg}'"
        ]

        context.log.info(cmd)

        proc = subprocess.Popen(
            args=cmd,
            cwd=BUILD_CWD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = proc.communicate()
        return_code = proc.returncode

        context.log.info(stdout)
        context.log.error(stderr)
        context.log.info(return_code)

        # # Checkout FEATURE
        # checkout_branch_msg = repo.git.checkout(branch)
        # context.log.info(f"Checkout: {checkout_branch_msg}")

    # if "Test failed with exit code 1" in stdout or return_code:
    # if return_code:
    #     raise Exception("rez unleash failed")

    yield MaterializeResult(
        asset_key=context.asset_key,
        metadata={
            # 'Test successful': MetadataValue.bool(True),
            'cwd': MetadataValue.path(BUILD_CWD),
            'cmd': MetadataValue.md(f"`{cmd}`"),
            'cmd (str)': MetadataValue.path(" ".join(cmd)),
            'environ (full)': MetadataValue.json(dict(os.environ)),
            # 'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
            # 'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
        }
    )
