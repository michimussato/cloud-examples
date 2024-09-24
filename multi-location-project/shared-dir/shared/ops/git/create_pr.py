import pathlib
import subprocess

from dagster import (
    op,
    In,
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue,
)


@op(
    ins={
        "BUILD_CWD": In(),
        "GH_EXE": In(),
        "PR_DRY_RUN": In(),
        "PR_READY_FOR_REVIEW": In(),
        "PR_ASSIGNEE": In(),
        "PR_REVIEWERS": In(),
        "BRANCH_NAME": In(),
        "AL_PACKAGE_PR": In(),
        "PR_BODY": In(),
        "rez_test": In(),
    },
)
def create_pr(
        context: AssetExecutionContext,
        BUILD_CWD: str,
        GH_EXE: str,
        PR_DRY_RUN: bool,
        PR_READY_FOR_REVIEW: bool,
        PR_ASSIGNEE: str,
        PR_REVIEWERS: list,
        BRANCH_NAME: str,
        AL_PACKAGE_PR: str,
        PR_BODY: str,
        rez_test: bool,  # DEPENDENCY; not actually used

) -> MaterializeResult:
    """
    Make sure that the dev branch exists on the remote.
    `rez test` will fail if not pushed prior.
    """

    reviewers = ",".join(PR_REVIEWERS)

    # http://127.0.0.1:3000/asset-groups~create_pr*%20%22PR_REVIEWERS%22%20%22PR_DRY_RUN%22%20%22PR_BODY%22%20%22AL_PACKAGE_PR%22/?open-nodes%5B%5D=ptp_432&open-nodes%5B%5D=ptp_432%3Adefault&open-nodes%5B%5D=PTP_432&open-nodes%5B%5D=PTP_432%3Adefault&open-nodes%5B%5D=PTP_432%3ABuild_Test_Package&open-nodes%5B%5D=PTP_432%3ATest_Environment&open-nodes%5B%5D=PTP_432%3ASend_Email&open-nodes%5B%5D=PTP_432%3APackage&open-nodes%5B%5D=__repository__%40PTP_432%3AEnvironment&open-nodes%5B%5D=PTP_432%3AEnvironment&open-nodes%5B%5D=PTP_432%3ATest_Group&open-nodes%5B%5D=__repository__%40PTP_432%3ATest_Group&open-nodes%5B%5D=PTP_432%3AAL_Vars&open-nodes%5B%5D=__repository__%40PTP_432%3AAL_Vars&open-nodes%5B%5D=PTP_432%3AAL_Env_Vars&open-nodes%5B%5D=PTP_432%3ATEST&open-nodes%5B%5D=PTP_432%3APackage_AL_otio&open-nodes%5B%5D=PTP_432%3AAL_Launcher&open-nodes%5B%5D=PTP_432%3AAL_Job&open-nodes%5B%5D=PTP_432%3AScripts&open-nodes%5B%5D=PTP_432%3ATODOs&open-nodes%5B%5D=PTP_432%3AAL_ENV_LAUNCHER&open-nodes%5B%5D=PTP_432%3AGIT&open-nodes%5B%5D=PTP_432%3AENV_PACKAGE__AL_otio%3AAL_PACKAGE_NAME&open-nodes%5B%5D=PTP_432%3AENV_PACKAGE__AL_otio&open-nodes%5B%5D=PTP_432%3AHello&open-nodes%5B%5D=__repository__%40PTP_432%3AHello&open-nodes%5B%5D=PTP_432%3Abuild_test_package__AL_otio&open-nodes%5B%5D=__repository__%40PTP_432%3Adefault&open-nodes%5B%5D=__repository__%40PTP_432%3Abuild_test_package__AL_otio&open-nodes%5B%5D=PTP_432%3Adefault%3Abuild_test_package__AL_otio&open-nodes%5B%5D=__repository__%40PTP_432%3Abuild_test_package__AL_vortex_library_edit&open-nodes%5B%5D=PTP_432%3Abuild_test_package__AL_vortex_library_edit&open-nodes%5B%5D=PTP_432%3Abuild_test_package__AL_vortex_library_edit%3Abuild_test_package__AL_vortex_library_edit%2Fbuild_test_package__AL_vortex_library_edit&open-nodes%5B%5D=PTP_432%3Abuild_test_packages&open-nodes%5B%5D=__repository__%40PTP_432%3AENV_PACKAGE__AL_otio&open-nodes%5B%5D=PTP_432%3AAL_otio&open-nodes%5B%5D=PTP_432%3AAL_PACKAGES&open-nodes%5B%5D=PTP_432%3AAL_vortex_library_edit&open-nodes%5B%5D=PTP_432%3Atesting_packages&open-nodes%5B%5D=__repository__%40PTP_432%3ABuild_Test_Package&open-nodes%5B%5D=PTP_432%3ASCRIPTS&open-nodes%5B%5D=PTP_432%3ASCRIPTS%3AEDIT_REPORT_TEST_SCRIPT&open-nodes%5B%5D=PTP_432%3Atesting_packages%3Ablack_formatter__AL_otio&open-nodes%5B%5D=PTP_432%3AAL_ENV_VARS&open-nodes%5B%5D=PTP_432%3ASend_Email%3Asend_email&open-nodes%5B%5D=PTP_432%3Adefault%3Aoverrides&open-nodes%5B%5D=PTP_432%3AAL_ENV_LAUNCHER_OVERRIDES&open-nodes%5B%5D=PTP_432%3Atesting_packages%3Arez_env_launcher_test_AL_otio&open-nodes%5B%5D=PTP_432%3ATest_Environment%3Aal_input_aaf&open-nodes%5B%5D=PTP_432%3Atesting_packages__AL_otio&open-nodes%5B%5D=PTP_432%3Atesting_packages__AL_vortex_library_edit&open-nodes%5B%5D=PTP_432%3Atesting_packages__AL_vortex_library_edit%3Acheck_branch_exists_on_remote_AL_vortex_library_edit&open-nodes%5B%5D=__repository__%40PTP_432%3AAL_vortex_library_edit&open-nodes%5B%5D=__repository__%40PTP_432%3AAL_otio&open-nodes%5B%5D=PTP_432%3AAL_PACKAGE__AL_vortex_library_edit&open-nodes%5B%5D=PTP_432%3AAL_PACKAGE__AL_otio&open-nodes%5B%5D=PTP_432%3AAL_PACKAGE__AL_otio%3AAL_otio%2FGIT_SSH&open-nodes%5B%5D=PTP_432%3AAL_PACKAGE__AL_vortex_library_edit%3AAL_vortex_library_edit%2FGIT_SSH&open-nodes%5B%5D=PTP_432%3ATODOs%3Arez_unleash&open-nodes%5B%5D=PTP_432%3A03__create_pr&open-nodes%5B%5D=PTP_432%3ATODOs_GIT&expanded=__repository__%40PTP_432%3A03__create_pr%2C__repository__%40PTP_432%3AAL_PACKAGE__AL_vortex_library_edit%2C__repository__%40PTP_432%3AAL_ENV_VARS%2C__repository__%40PTP_432%3A03__create_pr%2C__repository__%40PTP_432%3Atesting_packages__AL_otio%2C__repository__%40PTP_432%3Atesting_packages__AL_vortex_library_edit%2C__repository__%40PTP_432%3ATODOs_GIT%2C__repository__%40PTP_432%3AAL_PACKAGE__AL_otio&logFileKey=iemcoyqd

    if not AL_PACKAGE_PR:
        cmd = [
            GH_EXE,
            "pr",
            "create",
            "--assignee",
            f"{PR_ASSIGNEE}",
            "--reviewer",
            f"{reviewers}",
            "--title",
            f"{BRANCH_NAME}",
            "--body-file",
            PR_BODY,
        ]

        if PR_DRY_RUN:
            cmd.append(
                "--dry-run"
            )
        if not PR_READY_FOR_REVIEW:
            cmd.append(
                "--draft"
            )

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

        # if stderr:
        #     raise Exception(stderr)

        if bool(return_code):
            raise Exception("PR failed.")

        context.log.warning("Make sure you add the PR URL to `AL_PACKAGE_PR` "
                            "in `asset_factory_al_packages.py`. Otherwise, "
                            "you won't be able to edit this PR: "
                            f"{stdout}")

        yield MaterializeResult(
            asset_key=context.asset_key,
            metadata={
                'PR Body': MetadataValue.md(pathlib.Path(PR_BODY).read_text(encoding="utf-8")),
                'Reviewers': MetadataValue.text(reviewers),
                "Dry Run": MetadataValue.bool(PR_DRY_RUN),
                "Draft": MetadataValue.bool(not PR_READY_FOR_REVIEW),
                "PR": MetadataValue.url(stdout),
                'cmd': MetadataValue.md(f"`{cmd}`"),
                'cmd (str)': MetadataValue.path(" ".join(cmd)),
                'cwd': MetadataValue.path(BUILD_CWD),
                # 'repo': MetadataValue.path(repo),
                'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
                'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
            }
        )
    else:
        cmds = []

        # get reviewers:
        # gh pr view https://github.com/animallogic-rnd/vortexLibrary/pull/1966

        cmd = [
            GH_EXE,
            "pr",
            "edit",
            AL_PACKAGE_PR,
            "--body-file",
            PR_BODY,
        ]

        cmds.append(cmd)

        cmd_ready = [
            GH_EXE,
            "pr",
            "ready",
        ]
        if not PR_READY_FOR_REVIEW:
            cmd_ready.append("--undo")

        cmds.append(
            cmd_ready
        )

        for reviewer in PR_REVIEWERS:
            context.log.info(f"Adding reviewer: {reviewer}")
            cmd = [
                GH_EXE,
                "pr",
                "edit",
                AL_PACKAGE_PR,
                "--add-reviewer",
                reviewer,
            ]

            proc_reviewer = subprocess.Popen(
                args=cmd,
                cwd=BUILD_CWD,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout_reviewer, stderr_reviewer = proc_reviewer.communicate()
            return_code_reviewer = proc_reviewer.returncode

            context.log.info(stdout_reviewer)
            context.log.error(stderr_reviewer)
            context.log.info(return_code_reviewer)

        for cmd in cmds:

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

        yield MaterializeResult(
            asset_key=context.asset_key,
            metadata={
                'PR Body': MetadataValue.md(pathlib.Path(PR_BODY).read_text(encoding="utf-8")),
                'Reviewers': MetadataValue.text(reviewers),
                "Dry Run": MetadataValue.bool(PR_DRY_RUN),
                "Draft": MetadataValue.bool(not PR_READY_FOR_REVIEW),
                "PR": MetadataValue.url(AL_PACKAGE_PR),
            }
        )

        # if stderr:
        #     raise Exception(stderr)

    # if bool(return_code):
    #     raise Exception("PR failed.")
