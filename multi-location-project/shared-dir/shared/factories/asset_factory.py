from dagster import (
    asset,
    Output,
    AssetMaterialization,
    AssetsDefinition,
    RetryPolicy,
    Backoff,
    Jitter,
)


def asset_factory(group_name, spec) -> AssetsDefinition:

    @asset(
        group_name=group_name,
        key_prefix=spec["key_prefix"],
        name=spec["name"],
        deps=spec["deps"],
        # retry_policy=RetryPolicy(
        #     max_retries=5,
        #     delay=2,
        #     backoff=Backoff.EXPONENTIAL,
        #     jitter=Jitter.FULL,
        # ),
    )
    def _asset() -> dict:

        yield Output(spec["value"])

        yield AssetMaterialization(
            asset_key=[
                *spec["key_prefix"],
                spec["name"],
            ],
            metadata={
                spec["name"]: spec["type"](spec["value"]),
            },
        )

    return _asset
