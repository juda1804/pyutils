import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def obtener_novedades(numero_guia):
    # Prepara el payload para la solicitud POST
    payload = {
        "EncriptaAes": True,
        "IdOpcion": 0,
        "NumeroGuia": numero_guia,
        "NumeroTelefono": None
    }

    # Configura las cabeceras necesarias
    headers = {
        'accept': 'text/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/json',
        'origin': 'https://www3.interrapidisimo.com:8082',
        'priority': 'u=1, i',
        'referer': 'https://www3.interrapidisimo.com:8082/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
    }

    # Realiza la solicitud al servicio de Interrapidísimo
    response = requests.post('https://www3.interrapidisimo.com/ApiServInter/api/Mensajeria/ObtenerRastreoGuiasClientePost',
                             json=payload, headers=headers)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        return response.json()
    else:
        # En caso de error, devuelve el código de error y un mensaje
        return {'error': 'No se pudo obtener la información de rastreo', 'status_code': response.status_code}


def limpiar_cadena_personalizada(cadena):
    reemplazos = {
        '_2B': '+',
        '_2F': '/',
        '_3D': '='
    }
    for key, value in reemplazos.items():
        cadena = cadena.replace(key, value)
    return cadena

def rastrear_guia(numero_de_guia):
    # Configurar opciones para ejecutar Firefox en modo headless
    options = Options()
    options.headless = False  # Cambia a True para ejecutar en modo headless
    options.add_argument("--headless")  # Activa el modo headless de manera explícita
    options.add_argument("--disable-gpu")  # Deshabilita la GPU (opcional, por si acaso)
    options.add_argument("--no-sandbox")  # Agrega esta opción si estás ejecutando en un entorno sin UI

    service = FirefoxService(executable_path='/usr/bin/geckodriver')  # Asegúrate de que esta sea la ruta correcta

    driver = webdriver.Firefox(service=service, options=options)

    try:
        encrypted_track_id = "_2BY9HZx3rBZstOr_2BSlpkRTEqyp_2BI_2F6QHHC5qQ_2FRWbzEPoNw_2FsVfXXUNLoWN7FPb6EZZhDl6WumK3MALRbuW5fIA_3D_3D"
        url = 'https://www3.interrapidisimo.com:8082/SiguetuEnvio/shipment/'+encrypted_track_id
        driver.get(url)

        input_guide = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'inputGuide'))
        )

        input_guide.clear()
        input_guide.send_keys(numero_de_guia)

        elemento = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.right-button'))
        )

        elemento.click()
        time.sleep(1)

        # Captura la URL actual
        current_url = driver.current_url
        # print("current_url" + current_url, flush=True)
        # Extrae el último path parameter de la URL
        guia_encrypted = current_url.split('/')[-1]

        # print("encripted:" + guia_encrypted)
        resultado = limpiar_cadena_personalizada(guia_encrypted)
        # Muestra el último path parameter
        return {"guia_encrypted": resultado}

    except NoSuchElementException:
        print("El elemento no fue encontrado en la página.", flush=True)
    except TimeoutException:
        print("El elemento no fue encontrado o no es visible dentro del tiempo esperado.", flush=True)
    except Exception as e:
        return {"error": str(e)}
    #finally:
        # Cierra el navegador
        # driver.quit()