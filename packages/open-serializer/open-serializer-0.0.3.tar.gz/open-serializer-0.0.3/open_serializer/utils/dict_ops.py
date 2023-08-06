from __future__ import annotations


def merge_dict_recursively(
    base_attrs: dict,
    *addons_attrs: dict,
    force_replace: bool = False,
    skip_duplicated_list: bool = False,
) -> None:
    """Merge multiple dicts into the fist one.

    Args:
        base_attrs: the base dict to be merged into.
        addons_attrs: the dicts to be merged into the base dict.
        force_replace: whether to force replace the value in the base dict is conflict.
        skip_duplicated_list: whether to skip duplicated value when merging list.
    """

    for addons in addons_attrs:
        for key, value in addons.items():
            if key in base_attrs:
                if type(value) == type(base_attrs[key]):
                    if isinstance(value, list):
                        if skip_duplicated_list:
                            base_attrs[key].extend([v for v in value if v not in base_attrs[key]])
                        else:
                            base_attrs[key].extend(value)
                    elif isinstance(value, dict):
                        merge_dict_recursively(
                            base_attrs[key],
                            value,
                            force_replace=force_replace,
                            skip_duplicated_list=skip_duplicated_list,
                        )
                    else:
                        base_attrs[key] = value
                elif force_replace:
                    base_attrs[key] = value
            else:
                base_attrs[key] = value
