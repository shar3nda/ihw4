from fastapi import FastAPI, Request
from fastapi.responses import Response as FastAPIResponse
import httpx

app = FastAPI()
auth_service = "http://localhost:8081"
order_service = "http://localhost:8082"


async def proxy_request(request: Request, service_url: str, route: str):
    """
    Proxy request to another service asynchronously
    :param request: request object
    :param service_url: service url
    :param route: route to proxy
    :return: response from service
    """
    method = request.method
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(f"{service_url}/{route}", headers=headers)
        elif method == "POST":
            response = await client.post(
                f"{service_url}/{route}", data=await request.body(), headers=headers
            )
        elif method == "PUT":
            response = await client.put(
                f"{service_url}/{route}", data=await request.body(), headers=headers
            )
        elif method == "DELETE":
            response = await client.delete(f"{service_url}/{route}", headers=headers)
        else:
            return FastAPIResponse("Method not handled", status_code=500)

    return FastAPIResponse(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@app.get("/auth/{route}")
async def auth_route(request: Request, route: str):
    return await proxy_request(request, auth_service, route)


@app.get("/order/{route}")
async def order_route(request: Request, route: str):
    return await proxy_request(request, order_service, route)
