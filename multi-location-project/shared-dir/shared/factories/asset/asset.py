from dagster import (asset,
                     Output,
                     AssetMaterialization,
                     AssetsDefinition,
                     RetryPolicy,
                     Backoff,
                     Jitter,
                     MetadataValue,
                     )


def asset_factory(group_name, spec) -> AssetsDefinition:

    @asset(
        group_name=group_name,
        # key_prefix=spec["key_prefix"],
        name=spec["package_name"],
        # deps=spec["deps"],
        retry_policy=RetryPolicy(
            max_retries=5,
            delay=2,
            backoff=Backoff.EXPONENTIAL,
            jitter=Jitter.FULL,
        ),
    )
    def _asset() -> dict:

        # yield Output(spec["package_name"])
        yield Output(spec)

        yield AssetMaterialization(
            asset_key=[
                # *spec["key_prefix"],
                spec["package_name"],
            ],
            metadata={
                spec["package_name"]: MetadataValue.text(spec["package_name"]),
                spec["package_version"]: MetadataValue.text(spec["package_version"]),
            },
        )

    return _asset
