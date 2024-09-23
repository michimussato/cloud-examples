from dagster import Definitions, load_assets_from_modules

from . import assets
from . import from_factory


assets = load_assets_from_modules([assets])
from_factory = load_assets_from_modules([from_factory])

all_assets = [
    *assets,
    *from_factory,
]

defs = Definitions(
    assets=all_assets,
)
