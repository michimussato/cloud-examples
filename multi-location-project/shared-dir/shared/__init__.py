from dagster import (AssetExecutionContext,
                     # MaterializeResult,
                     AssetMaterialization,
                     Output,
                     MetadataValue)


def shared_function(
        context: AssetExecutionContext,
        **kwargs
) -> AssetMaterialization:

    yield Output("Return Value")

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "kwargs": MetadataValue.json(kwargs)
        }
    )


# def shared_function(
#         context: AssetExecutionContext,
#         **kwargs
# ) -> MaterializeResult:
#     return MaterializeResult()
