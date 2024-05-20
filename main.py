from faker import Faker
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep, strftime
from polideportivos_data import supported_polis

fake = Faker(["es_AR"])

# Dependiendo de la velocidad de tu computadora ajustar la velocidad
SPEED = 4


def get_random_dni():
    return randint(10000000, 50000000)


def get_browser():
    return webdriver.Firefox(
        service=Service(GeckoDriverManager().install()))


def get_person_trait(trait_name):
    trait = ""

    if trait_name == "first_name":
        trait = fake.first_name()
    elif trait_name == "last_name":
        trait = fake.last_name()
    elif trait_name == "email":
        trait = fake.ascii_free_email()

    return trait


def get_poli_idx(polis):
    for idx, value in enumerate(polis):
        print(f"{idx} - Polideportivo {value["name"]}")

    return int(input("Ingrese el numero del polideportivo deseado: "))


def get_cancha_size(poli_canchas):
    for idx, value in enumerate(poli_canchas):
        print(f"{idx} - Cancha Futbol {value}")

    cancha_idx = int(input("Ingrese el numero de la cancha deseada: "))

    return poli_canchas[cancha_idx]


def get_cancha_type(poli_tipos):
    for idx, value in enumerate(poli_tipos):
        print(f"{idx} - {value}")

    tipo_idx = int(input("Ingresar el tipo de cancha: "))

    return poli_tipos[tipo_idx]


def get_cancha_sport(poli_sports):
    for idx, value in enumerate(poli_sports):
        print(f"{idx} - {value}")

    sport_idx = int(input("Ingresar el deporte de cancha: "))

    return poli_sports[sport_idx]


def main():
    # Ingresar el polideportivo
    poli_idx = get_poli_idx(supported_polis)
    poli = supported_polis[poli_idx]

    # Ingresar informacion de la cancha y el usuario
    cancha_sport = get_cancha_sport(list(poli["urls"].keys()))
    cancha_day = input("Ingresar dia de reserva de la cancha: ")
    cancha_hour = input("Ingresar la hora de reserva de la cancha: ")
    if cancha_sport == "Futbol":
        cancha_size = get_cancha_size(poli["canchas"])
        cancha_type = get_cancha_type(poli["tipos"])
    user_email = input("Ingresar el email de tu cuenta miBA: ")
    user_password = input("Ingresar la contraseña de tu cuenta miBA: ")
    driver = get_browser()

    # Entrar a la pagina de la cancha
    driver.get(poli["urls"][cancha_sport])
    sleep(SPEED)

    # Si tiene una sola cancha clickearla, si son mas elegirla
    if len(poli["canchas"]) == 1 or cancha_sport == "Basquet":
        texto_anchor = "Reservá tu turno"
    else:
        texto_anchor = f"fútbol {cancha_size}"
    driver.find_element(
        By.XPATH, f"//a[contains(text(), '{texto_anchor}')]").click()
    sleep(SPEED)

    # Loguearse con email
    driver.find_element(By.ID, "zocial-mail").click()
    sleep(SPEED)

    # Ingresar email, contraseña y dar click en el button de login
    driver.find_element(By.ID, "email").send_keys(user_email)
    driver.find_element(By.ID, "password-text-field").send_keys(user_password)
    driver.find_element(By.ID, "login").click()
    sleep(SPEED)

    # Clickear en el link de elegir cancha for fecha
    driver.find_element(By.XPATH, "//div[@data-start='fecha']").click()
    sleep(SPEED)

    # Elegir dia de la cancha
    month = strftime("%m")
    year = strftime("%Y")
    driver.find_element(
        By.XPATH, f"//h4[@data-date='{year}-{month}-{cancha_day}']").click()
    sleep(SPEED)

    # Elegir cancha dependiendo del polideportivo
    if cancha_sport == "Futbol" and cancha_type:
        driver.find_element(
            By.XPATH, f"//input[contains(@data-placename, '{cancha_type}')]"
        ).click()
        sleep(SPEED)

    # Clickear en el boton de guardar y continuar
    driver.find_element(By.ID, "save").click()
    sleep(SPEED)

    # Elegir hora de la cancha
    driver.find_element(
        By.XPATH, f"//input[@data-hour='{cancha_hour}:00']").click()
    sleep(SPEED)

    # Clickear en el boton de siguiente
    driver.find_element(By.ID, "next").click()
    sleep(SPEED)

    # Elegir todos los inputs de nombre, apellido, email y dni
    nombre_inputs = driver.find_elements(
        By.XPATH, "//input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'form_nombre')]"

    )
    apellido_inputs = driver.find_elements(
        By.XPATH, "//input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'form_apellido')]"
    )
    email_inputs = driver.find_elements(
        By.XPATH, "//input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'form_email')]"
    )
    dni_inputs = driver.find_elements(
        By.XPATH, "//input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'form_tipoynrodoca')][@type='number']"
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
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Siguiente')]").click()
    sleep(SPEED)

    # Clickear en el boton de confirmar turno
    driver.find_element(By.ID, "confirmarTurno").click()
    sleep(SPEED)

    # Clickear en el boton de siguiente
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Finalizar')]").click()

    # Cerrar navegador e informar que se reservo exitosamente
    driver.close()
    print("Se reservo la cancha exitosamente!")


if __name__ == "__main__":
    main()
