from faker import Faker
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, strftime
from polideportivos_data import polis

fake = Faker(["es_AR"])

supported_browsers = [{"name": "Firefox"}, {"name": "Chrome"}]

SPEED = 2


def get_person_trait(trait_name):
    trait = ""

    if trait_name == "first_name":
        trait = fake.first_name()
    elif trait_name == "last_name":
        trait = fake.last_name()
    elif trait_name == "email":
        trait = fake.ascii_free_email()

    return trait

def get_random_dni():
    return randint(10000000, 47000000)


def get_poli_url():
    for idx in range(len(polis)):
        print(f"{idx} - Polideportivo {polis[idx]["name"]}")

    return int(input("Ingrese el numero del polideportivo deseado: "))


def get_cancha_size(poli_idx):
    canchas = polis[poli_idx]["canchas"]

    for idx in range(len(canchas)):
        print(f"{idx} - Cancha futbol {canchas[idx]}")
    cancha_idx = int(input("Ingrese el numero de la cancha deseada: "))

    return canchas[cancha_idx]


def get_cancha_type(poli_idx):
    poli_name = polis[poli_idx]["name"]
    cancha_type = ""
    
    if poli_name == "Parque Patricios":
        print("0 - Asfalto")
        print("1 - Sintetico")
        cancha_type = int(input("Ingresar el tipo de cancha: "))
    elif poli_name == "Martin Fierro":
        print("0 - Cancha 1")
        print("1 - Cancha 2")
        cancha_type = int(input("Ingresar el numero de cancha: "))

    return cancha_type


def get_browser_name():
    for idx in range(len(supported_browsers)):
        print(f"{idx} - {supported_browsers[idx]['name']}")
    browser_idx = int(input("Ingrese el numero del navegador web a utilizar: "))

    return supported_browsers[browser_idx]["name"]


def get_browser():
    browser_name = get_browser_name()
    browser = ""

    if browser_name == "Firefox":
        browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    elif browser_name == "Chrome":
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    return browser


def main():
    poli_idx = get_poli_url()
    cancha_day = input("Ingresar dia de reserva de la cancha: ")
    cancha_hour = input("Ingresar la hora de reserva de la cancha: ")
    cancha_size = get_cancha_size(poli_idx)
    cancha_type = get_cancha_type(poli_idx)
    user_email = input("Ingresar el email de tu cuenta miBA: ")
    user_password = input("Ingresar la contraseña de tu cuenta miBA: ")
    driver = get_browser()

    # Entrar a la pagina de la cancha
    driver.get(polis[poli_idx]["url"])

    # Si tiene una sola cancha clickearla, si son mas elegirla
    if len(polis[poli_idx]["canchas"]) == 1:
        driver.find_element(
            By.PARTIAL_LINK_TEXT,
            "https://formulario-sigeci.buenosaires.gob.ar/InicioTramite?idPrestacion=",
        ).click()
    else:
        # t = f"//a[contains(text(), 'fútbol {cancha_size}')]"
        driver.find_element(
            By.XPATH, f"//a[contains(text(), 'fútbol {cancha_size}')]"
        ).click()
    sleep(SPEED)

    # Loguearse con email
    driver.find_element(By.ID, "zocial-mail").click()
    sleep(SPEED)

    # Ingresar email, contrasena y dar click en el button de login
    driver.find_element(By.ID, "email").send_keys(user_email)
    driver.find_element(By.ID, "password-text-field").send_keys(user_password)
    driver.find_element(By.ID, "login").click()
    sleep(SPEED)

    #     driver.find_element(By.XPATH, "//input[contains(@id, 'form_email')]")
    # Clickear en el link de elegir cancha for fecha
    driver.find_element(By.XPATH, "//div[@data-start='fecha']").click()
    sleep(SPEED)

    # Elegir dia de la cancha
    month = strftime("%m")
    year = strftime("%Y")
    driver.find_element(By.XPATH, f"//h4[@data-date='{year}-{month}-{cancha_day}']").click()
    sleep(SPEED)

    # Elegir cancha dependiendo del polideportivo
    if cancha_type:
        driver.find_element(
            By.XPATH, f"//input[contains(@data-placename, '{cancha_type}')]"
        ).click()
        sleep(SPEED)

    # Clickear en el boton de guardar y continuar
    driver.find_element(By.ID, "save").click()
    sleep(SPEED)

    # Elegir hora de la cancha
    driver.find_element(By.XPATH, f"//input[@data-hour='{cancha_hour}:00']").click()
    sleep(SPEED)

    # Clickear en el boton de siguiente
    driver.find_element(By.ID, "next").click()
    sleep(SPEED)

    # Elegir todos los inputs de nombre, apellido, email y dni
    nombre_inputs = driver.find_elements(
        By.XPATH, "//input[contains(@id, 'form_Nombre')]"
    )
    apellido_inputs = driver.find_elements(
        By.XPATH, "//input[contains(@id, 'form_Apellido')]"
    )
    email_inputs = driver.find_elements(
        By.XPATH, "//input[contains(@id, 'form_Email')]"
    )
    dni_inputs = driver.find_elements(
        By.XPATH, "//input[contains(@id, 'form_TipoyNroDocA')][@type='number']"
    )
    sleep(SPEED)

    # Rellenar todos los inputs de nombre, apellido, email y dni con datos falsos de Faker
    for nombre_input in nombre_inputs:
        nombre_input.send_keys(get_person_trait("first_name"))

    for apellido_input in apellido_inputs:
        apellido_input.send_keys(get_person_trait("last_name"))

    for email_input in email_inputs:
        email_input.send_keys(get_person_trait("email"))

    for dni_input in dni_inputs:
        dni_input.send_keys(get_random_dni())

    # Clickear en el boton de siguiente
    driver.find_element(By.XPATH, "//button[contains(text(), 'Siguiente')]").click()
    sleep(SPEED)

    # Clickear en el boton de confirmar turno
    driver.find_element(By.ID, "confirmarTurno").click()
    sleep(SPEED)

    # Clickear en el boton de siguiente
    driver.find_element(By.XPATH, "//button[contains(text(), 'Finalizar')]").click()

    # Cerrar navegador e informar que se reservo exitosamente
    driver.close()
    print("Se reservo la cancha exitosamente!")

if __name__ == "__main__":
    main()
