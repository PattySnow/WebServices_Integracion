from fastapi import FastAPI, HTTPException, Path, Body
import requests

app = FastAPI()

@app.post("/webpay/create-transaction", tags=['Webpay'])
async def create_transaction(buy_order: str, session_id: str, amount: int, return_url: str):
    try:
        # URL de la API de Transbank para crear una transacción
        transbank_url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
        
        # Encabezados requeridos para la solicitud POST a Transbank
        headers = {
            "Tbk-Api-Key-Id": "597055555532",
            "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            "Content-Type": "application/json"
        }
        
        # Datos del cuerpo de la solicitud POST
        data = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount,
            "return_url": return_url
        }
        
        # Realizar una solicitud POST a la API de Transbank para crear una transacción
        response = requests.post(transbank_url, headers=headers, json=data)
        
        # Verificar el código de estado de la respuesta de Transbank
        if response.status_code == 200:
            # Devolver la respuesta de Transbank a la aplicación
            return response.json()
        else:
            # En caso de que la solicitud no sea exitosa, levantar una excepción HTTP
            raise HTTPException(status_code=response.status_code, detail="Error al crear la transacción en Transbank")
    except Exception as e:
        # Capturar cualquier excepción y devolver un mensaje de error genérico
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Ruta para obtener detalles de una transacción en la API de Transbank
@app.get("/webpay/get-transaction/{token}", tags=['Webpay'])
async def get_transaction(token: str = Path(..., description="Token de la transacción")):
    try:
        # URL completa de la API REST externa de Transbank para obtener detalles de transacciones
        api_url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
        
        # Encabezados necesarios para la solicitud GET a la API de Transbank
        headers = {
            "Tbk-Api-Key-Id": "597055555532",
            "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        }
        
        # Realizar una solicitud GET a la API de Transbank para obtener detalles de la transacción
        response = requests.get(api_url, headers=headers)
        
        # Verificar el código de estado de la respuesta de la API de Transbank
        if response.status_code == 200:
            # Devolver los datos obtenidos de la API de Transbank
            return response.json()
        else:
            # En caso de que la solicitud no sea exitosa, levantar una excepción HTTP
            raise HTTPException(status_code=response.status_code, detail="Error al obtener detalles de la transacción en Transbank")
    except Exception as e:
        # Capturar cualquier excepción y devolver un mensaje de error genérico
        raise HTTPException(status_code=500, detail="Error interno del servidor")