from cowsay import main

from dagster import asset, AssetIn

from shared import shared_function


# noinspection PyArgumentList
s1 = asset(
    compute_fn=shared_function,
    name="shared1",
    compute_kind="youtube",
    ins={
        "asset1": AssetIn(),
    },
)


# noinspection PyArgumentList
s2 = asset(
    compute_fn=shared_function,
    name="shared2",
    compute_kind="yaml",  # https://sourcegraph.com/github.com/dagster-io/dagster/-/blob/js_modules/dagster-ui/packages/ui-core/src/graph/OpTags.tsx
    ins={
        "asset1": AssetIn(),
    },
)


@asset
def asset1(context):
    # context.log.info(shared_function())
    context.log.info(f"Cowsay version {main.__version__}")
