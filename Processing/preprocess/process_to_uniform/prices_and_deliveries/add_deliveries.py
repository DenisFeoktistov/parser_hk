import copy


def add_deliveries(skus):
    new_skus = copy.deepcopy(skus)

    for sku in new_skus:
        sku["delivery_info"] = dict()
        sku["delivery_info"]["platform"] = "poizon"
        sku["delivery_info"]["min_platform_delivery"] = 3
        sku["delivery_info"]["max_platform_delivery"] = 5

    return new_skus

