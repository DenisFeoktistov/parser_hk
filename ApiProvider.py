import json

import aiohttp
import requests


class ApiProvider:
    API_HOST = "https://sellout.su/hg"

    @staticmethod
    def search(sku):
        return requests.get(f"{ApiProvider.API_HOST}/api/v1/search?q={sku}").json()

    @staticmethod
    def spuDetail(spuId):
        return requests.get(f"{ApiProvider.API_HOST}/api/v1/spuDetail?id={spuId}").json()

    @staticmethod
    def table(spuId):
        return requests.get(f"{ApiProvider.API_HOST}/api/v1/sizeTab?id={spuId}").json()

    @staticmethod
    def product(spuId):
        return requests.get(f"{ApiProvider.API_HOST}/api/v1/product?id={spuId}").json()

    @staticmethod
    async def async_search(sku):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ApiProvider.API_HOST}/api/v1/search?q={sku}") as response:
                return json.loads(await response.text())

    @staticmethod
    async def async_spu_detail(spuId):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ApiProvider.API_HOST}/api/v1/spuDetail?id={spuId}") as response:
                return json.loads(await response.text())

    @staticmethod
    async def async_product(spuId):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ApiProvider.API_HOST}/api/v1/product?id={spuId}") as response:
                return json.loads(await response.text())

    @staticmethod
    async def async_table(spuId):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ApiProvider.API_HOST}/api/v1/sizeTab?id={spuId}") as response:
                return json.loads(await response.text())
