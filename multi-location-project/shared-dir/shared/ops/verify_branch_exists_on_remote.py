from dagster import (op,
                     In,
                     # AssetExecutionContext,
                     OpExecutionContext,
                     Output,
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
def verify_branch_exists_on_remote(
        # context: AssetExecutionContext,
        context: OpExecutionContext,
        BRANCH_NAME: str,
        AL_PACKAGE_NAME: str,
        GIT_SSH: str,

) -> bool:
    """
    Make sure that the dev branch exists on the remote.
    `rez test` will fail if not pushed prior.
    """

    yield Output(True)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            'some metadata': MetadataValue.bool(True),
        }
    )


# Example:
# verify_branch_exists_on_remote_AL_otio = AssetsDefinition.from_op(
#     verify_branch_exists_on_remote,
#     group_name="testing_packages__AL_otio",
#     keys_by_input_name={
#         "BRANCH_NAME": AssetKey("BRANCH_NAME"),
#         "AL_PACKAGE_NAME": AssetKey(
#             ["AL_otio", "AL_PACKAGE_NAME"]
#         ),
#         "GIT_SSH": AssetKey(
#             ["AL_otio", "GIT_SSH"]
#         ),
#     },
#     keys_by_output_name={
#         "result": AssetKey("verify_branch_exists_on_remote_AL_otio"),
#     },
# )
