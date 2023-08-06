from test_all import test_function, test_dependencies

from tests.data.geolayers import (
    geolayer_fr_dept_data_only,
    geolayer_fr_dept_data_and_geometry,
    geolayer_fr_dept_data_and_geometry_4326_precision_6
)

from tests.data.fields_metadata import geolayer_data_fields_metadata_complete

from geoformat.conversion.feature_conversion import feature_serialize

from geoformat.conversion.geolayer_conversion import (
    create_geolayer_from_i_feat_list,
    reproject_geolayer,
)

create_geolayer_from_i_feat_list_parameters = {
    0: {
        "geolayer": geolayer_fr_dept_data_only,
        "i_feat_list": 0,
        "serialize": False,
        "reset_i_feat": True,
        "return_value": {
            "metadata": {
                "fields": geolayer_data_fields_metadata_complete,
                "name": "FRANCE_DPT_GENERALIZE_LAMB93_ROUND_DATA_ONLY",
            },
            "features": {0: {"attributes": {"CODE_DEPT": "32", "NOM_DEPT": "GERS"}}},
        },
    },
    1: {
        "geolayer": geolayer_fr_dept_data_only,
        "i_feat_list": [0],
        "serialize": False,
        "reset_i_feat": True,
        "return_value": {
            "metadata": {
                "fields": geolayer_data_fields_metadata_complete,
                "name": "FRANCE_DPT_GENERALIZE_LAMB93_ROUND_DATA_ONLY",
            },
            "features": {0: {"attributes": {"CODE_DEPT": "32", "NOM_DEPT": "GERS"}}},
        },
    },
    2: {
        "geolayer": geolayer_fr_dept_data_only,
        "i_feat_list": [0, 95],
        "serialize": False,
        "reset_i_feat": True,
        "return_value": {
            "metadata": {
                "fields": geolayer_data_fields_metadata_complete,
                "name": "FRANCE_DPT_GENERALIZE_LAMB93_ROUND_DATA_ONLY",
            },
            "features": {
                0: {"attributes": {"CODE_DEPT": "32", "NOM_DEPT": "GERS"}},
                1: {"attributes": {"CODE_DEPT": "93", "NOM_DEPT": "SEINE-SAINT-DENIS"}},
            },
        },
    },
    3: {
        "geolayer": geolayer_fr_dept_data_only,
        "i_feat_list": [0, 95],
        "serialize": False,
        "reset_i_feat": False,
        "return_value": {
            "metadata": {
                "fields": geolayer_data_fields_metadata_complete,
                "name": "FRANCE_DPT_GENERALIZE_LAMB93_ROUND_DATA_ONLY",
            },
            "features": {
                0: {"attributes": {"CODE_DEPT": "32", "NOM_DEPT": "GERS"}},
                95: {
                    "attributes": {"CODE_DEPT": "93", "NOM_DEPT": "SEINE-SAINT-DENIS"}
                },
            },
        },
    },
    4: {
        "geolayer": geolayer_fr_dept_data_only,
        "i_feat_list": [0, 95],
        "serialize": True,
        "reset_i_feat": False,
        "return_value": {
            "metadata": {
                "fields": geolayer_data_fields_metadata_complete,
                "name": "FRANCE_DPT_GENERALIZE_LAMB93_ROUND_DATA_ONLY",
            },
            "features": {
                0: feature_serialize(
                    {"attributes": {"CODE_DEPT": "32", "NOM_DEPT": "GERS"}}
                ),
                95: feature_serialize(
                    {"attributes": {"CODE_DEPT": "93", "NOM_DEPT": "SEINE-SAINT-DENIS"}}
                ),
            },
        },
    },
}

reproject_geolayer_parameters = {
    0: {
        "geolayer": geolayer_fr_dept_data_and_geometry,
        "out_crs": 4326,
        "in_crs": None,
        "precision": 6,
        "return_value": geolayer_fr_dept_data_and_geometry_4326_precision_6
    },
    1: {
        "geolayer": geolayer_fr_dept_data_and_geometry,
        "out_crs": 4326,
        "in_crs": 2154,
        "precision": 6,
        "return_value": geolayer_fr_dept_data_and_geometry_4326_precision_6
    },
}


def test_all():
    # create_geolayer_from_i_feat_list
    print(
        test_function(
            create_geolayer_from_i_feat_list,
            create_geolayer_from_i_feat_list_parameters,
        )
    )

    # reproject_geolayer
    print(test_function(reproject_geolayer, reproject_geolayer_parameters))


if __name__ == "__main__":
    test_all()




