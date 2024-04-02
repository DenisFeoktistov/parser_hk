from fastapi import FastAPI
import uvicorn


from Processing.process_sku import process_sku


api_app = FastAPI()


@api_app.get("/parser_hk_api/process_sku")
async def process_sku_api(sku: str):
    result = await process_sku(sku)

    return result


if __name__ == "__main__":
    uvicorn.run(api_app, host='0.0.0.0', port=5000)
