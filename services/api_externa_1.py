import httpx

# Exemplo de cliente HTTP para API externa
async def buscar_dados_externos(param: str):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"https://api.exemplo.com/{param}")
        response.raise_for_status()
        return response.json()