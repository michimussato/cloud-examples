from dagster import Definitions, load_assets_from_modules

from . import from_assets
from . import from_factory
from . import from_op


# From resources_examples
from shared.resources_examples.show_definition import get_show_assets
from .dummies import dummies


assets = load_assets_from_modules([from_assets])
from_factory = load_assets_from_modules([from_factory])
from_op = load_assets_from_modules([from_op])

dummies = load_assets_from_modules([dummies])


all_assets = [
    *assets,
    *from_factory,
    *from_op,
    *get_show_assets(),
    *dummies,
]

defs = Definitions(
    assets=all_assets,
)
