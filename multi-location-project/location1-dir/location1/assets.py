from cowsay import main

from dagster import asset, AssetIn

from shared import shared_function


s1 = asset(
    compute_fn=shared_function,
    name="shared1",
    ins={
        "asset1": AssetIn(),
    },
)

s2 = asset(
    compute_fn=shared_function,
    name="shared2",
    ins={
        "asset1": AssetIn(),
    },
)


@asset
def asset1(context):
    # context.log.info(shared_function())
    context.log.info(f"Cowsay version {main.__version__}")
