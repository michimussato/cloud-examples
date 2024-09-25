from dagster import (asset)


GROUP_NAME = "DUMMIES"


@asset(
    group_name=GROUP_NAME,
)
def BRANCH_NAME() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def GIT_REPO_NAME() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def MASTER_BRANCH() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def LOCAL_GIT_REPO_DIR() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def BUILD_CWD() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def RND_PACKAGES() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def AL_PACKAGE_NAME() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def AL_PACKAGE_VERSION() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def REZ_EXE() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def black() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def black_formatter__AL_affected_package_1() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def black_formatter__AL_affected_package_2() -> None:
    raise NotImplementedError


@asset(
    group_name=GROUP_NAME,
)
def black_formatter__AL_vortex_library_edit() -> None:
    raise NotImplementedError
