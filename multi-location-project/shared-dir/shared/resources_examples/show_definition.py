from shared.factories.asset_factory import asset_factory

from dagster import (MetadataValue,
                     AssetsDefinition,
                     )


JOB = "al_template"
SCENE = "zin01"
LOCATION = "alfx"
VERSION = "027"


show_dict = {
    "group_name": f"{LOCATION}_{JOB}_{SCENE}_{VERSION}",
    "assets": [
        # # Template:
        # {
        #     "name": ,
        #     "key_prefix": [],
        #     "value": ,
        #     "type": MetadataValue.,
        #     "deps": {},
        # },
        {
            "name": "AL_JOB",
            "key_prefix": [],
            "value": JOB,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            "name": "AL_SCENE",
            "key_prefix": [],
            "value": SCENE,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            "name": "AL_LOCATION",
            "key_prefix": [],
            "value": LOCATION,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            "name": "AL_INPUT_PATH",
            "key_prefix": [],
            "value": f'/jobs/{LOCATION}/{JOB}/{SCENE}/assets/fragment/edit/edit/scene/animatic/data/{SCENE}_edit_edit_scene_animatic_data_v{VERSION}',
            "type": MetadataValue.path,
            "deps": {},
        },
    ]
}


def get_show_assets() -> list[AssetsDefinition]:
    show_assets = [
        asset_factory(
            group_name=f"AL_SHOW__{show_dict['group_name']}",
            spec=spec,
        ) for spec in show_dict["assets"]
    ]
    return show_assets


if __name__ == "__main__":
    get_show_assets()
