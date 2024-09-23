from shared.resources_examples.package_definition import get_package_assets
from .packages.affected_package_1 import get_package_assets as AL_affected_package_1
from .packages.affected_package_2 import get_package_assets as AL_affected_package_2


# Example
assets_from_factory = get_package_assets()


AL_affected_package_1 = AL_affected_package_1()
AL_affected_package_2 = AL_affected_package_2()
