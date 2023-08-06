from typing import Optional, Union, Any, Dict

from algoralabs.data.sdr import APIFieldFilter, FieldFilter, LogicalDisplayName, DataFilter


def __transform_filter(filter: Union[FieldFilter, APIFieldFilter]) -> APIFieldFilter:
    if isinstance(filter, APIFieldFilter):
        return filter

    return APIFieldFilter(
        logical_display=LogicalDisplayName(
            logical_name=filter.field,
            display_name=filter.field
        ),
        operator=filter.operator,
        selected_values=filter.selected_values
    )


def transform_data_filter(data_filter: Optional[DataFilter]) -> Optional[Dict[str, Any]]:
    if data_filter is not None:
        transformed_filter = DataFilter(
            date_range=data_filter.date_range,
            filters=list(map(__transform_filter, data_filter.filters))
        )

        return transformed_filter.dict()

    return None
