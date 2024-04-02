import copy


REQUIRED_KEYS = ["skuId", "spuId", "propertyDesc", "stripped_name", "zh_price", "delivery_info"]


def remove_extra_info(skus):
    new_skus = copy.deepcopy(skus)

    for sku in new_skus:
        keys_to_delete = list()

        for key in sku:
            if key not in REQUIRED_KEYS:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del sku[key]

    return new_skus
