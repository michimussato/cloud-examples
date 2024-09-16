from cowsay import main

from dagster import asset, AssetIn
from shared import shared_function


s3 = asset(
    compute_fn=shared_function,
    name="shared3",
    ins={
        "asset2": AssetIn(),
    },
)

s4 = asset(
    compute_fn=shared_function,
    name="shared4",
    ins={
        "asset2": AssetIn(),
    },
)

@asset
def asset2(context):
    # context.log.info(shared_function())
    context.log.info(f"Cowsay version {main.__version__}")
