
def _get_recast_field_type_mapping(fields_metadata, geoformat_type_to_output_driver_type):
    """
    From geolayer field's metadata to output driver recast dict

    :param fields_metadata: geolayer field's metadata
    :param geoformat_type_to_output_driver_type: dict that make translation between geoformat type and output driver
    type

    :return: dict that allow to recast field
    """
    recast_field_mapping = {}
    if fields_metadata:
        for field_name, field_metadata in fields_metadata.items():
            recast_to_python_type = geoformat_type_to_output_driver_type.get(field_metadata['type'], None)
            if recast_to_python_type is not None:
                recast_field_mapping[field_name] = {
                    "recast_value_to_python_type": recast_to_python_type,
                    "resize_value_width": None,
                    "resize_value_precision": None
                }

    return recast_field_mapping
