from faker import Faker
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from polideportivos_data import polis

fake = Faker(["es_AR"])

supported_browsers = [{"name": "Firefox"}, {"name": "Chrome"}]

SPEED = 2


def get_person_trait(trait):
    if trait == "first_name":
        return fake.first_name()
    elif trait == "last_name":
        return fake.last_name()
    elif trait == "email":
        return fake.ascii_free_email()


def get_random_dni():
    return randint(10000000, 47000000)


def get_poli_url():
    for i, poli in enumerate(polis):
        print(f"{i} - Polideportivo {polis[i]['name']}")
    return int(input("Ingrese el numero del polideportivo deseado: "))


def get_cancha_size(poli_idx):
    canchas = polis[poli_idx]["canchas"]
    for i, poli in enumerate(canchas):
        print(f"{i} - Cancha futbol {canchas[i]}")
    cancha_idx = int(input("Ingrese el numero de la cancha deseada: "))
    return canchas[cancha_idx]


def get_browser_name():
    for i, poli in enumerate(supported_browsers):
        print(f"{i} - {supported_browsers[i]['name']}")
    browser_idx = int(input("Ingrese el numero del navegador web a utilizar: "))
    return supported_browsers[browser_idx]["name"]


def get_browser():
    browser_name = get_browser_name()
    if browser_name == "Firefox":
        return webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    elif browser_name == "Chrome":
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def main():
    poli_idx = get_poli_url()
    cancha_day = input("Ingresar dia de reserva de la cancha: ")
    cancha_hour = input("Ingresar la hora de reserva de la cancha: ")
    cancha_size = get_cancha_size(poli_idx)
    if polis[poli_idx]["name"] == "Parque Patricios":
        cancha_type = input("Ingresar el tipo de cancha, elegir asfalto o sintetico: ")
    elif polis[poli_idx]["name"] == "Martin Fierro":
        cancha_type = input("Ingresar numero de cancha, 1 o 2: ")
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
    driver.find_element(By.XPATH, f"//h4[@data-date='2024-02-{cancha_day}']").click()
    sleep(SPEED)

    # Elegir cancha dependiendo del polideportivo
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


if __name__ == "__main__":
    main()
