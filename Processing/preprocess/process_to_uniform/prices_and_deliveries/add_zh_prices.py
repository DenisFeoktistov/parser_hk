import copy

from Processing.preprocess.process_to_uniform.prices_and_deliveries.hg_to_zh_price import hg_to_zh


def add_zh_prices(skus):
    new_skus = copy.deepcopy(skus)

    for sku in new_skus:
        sku["zh_price"] = None

        if "price" in sku:
            price = float(sku["price"]["money"]["amount"])

            sku["zh_price"] = hg_to_zh(price)

    return new_skus
