from faker import Faker
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep, strftime
from datetime import datetime
from polideportivos_data import supported_polis

fake = Faker(["es_AR"])

# Dependiendo de la velocidad de tu computadora ajustar la velocidad
SPEED = 1
# Se utiliza translate para volver el texto del id a minusculas
ID_TO_LOWERCASE = "translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"


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
    elif trait_name == "domicilio":
        trait = fake.street_address()
    elif trait_name == "localidad":
        trait = fake.municipality()
    elif trait_name == "barrio":
        trait = fake.street_municipality()
    elif trait_name == "fecha_nacimiento":
        # Devolver fecha entre 1970 y 2000, con formato "1999-05-30"
        start_date = datetime(1970, 1, 1)
        end_date = datetime(2007, 1, 1)
        trait = fake.date_between(start_date, end_date).strftime("%Y-%m-%d")

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


def rellenar_nombres(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_nombre')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("first_name"))


def rellenar_fechas_nacimiento(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_fechanacasistente')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("fecha_nacimiento"))


def rellenar_apellidos(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_apellido')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("last_name"))


def rellenar_localidades(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_localidad')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("localidad"))


def rellenar_barrios(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_barrio')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("barrio"))

    # Input que tiene diferente id a los otros
    input_extra = driver.find_element(By.ID, 'form_Comuna')
    input_extra.send_keys(get_person_trait("barrio"))


def rellenar_dnis(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_tipoynrodoca')][@type='number']"
    )
    for input in inputs:
        input.send_keys(get_random_dni())


def rellenar_emails(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_email')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("email"))


def rellenar_domicilios(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_domicilio')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("domicilio"))


def rellenar_telefonos(driver):
    inputs = driver.find_elements(
        By.XPATH, f"//input[contains({ID_TO_LOWERCASE}, 'form_telefono')]"
    )
    for input in inputs:
        input.send_keys(get_person_trait("domicilio"))


def rellenar_cantidad_asistentes(driver):
    # Seleccionar el valor de 4 asistentes del select dropdown
    cantidad_asistentes = Select(driver.find_element(By.ID, "form_CantidadAsistentes"))
    cantidad_asistentes.select_by_value("4")    


def main():
    # Ingresar el polideportivo
    poli_idx = get_poli_idx(supported_polis)
    poli = supported_polis[poli_idx]

    # Ingresar informacion de la cancha y el usuario
    cancha_sport = get_cancha_sport(list(poli["urls"].keys()))
    cancha_day = input("Ingresar dia de reserva de la cancha: ")
    cancha_hour = input("Ingresar la hora de reserva de la cancha: ")
    cancha_month = input("Ingresar el mes de reserva de la cancha: ")
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
    if len(poli["canchas"]) == 1 or (cancha_sport in ["Basquet", "Tennis"]):
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

    # Elegir mes
    driver.find_element(By.ID, "monthSelected").click()
    sleep(SPEED)

    driver.find_element(By.XPATH, f"//p[@data-month='{cancha_month}']").click()

    # Elegir dia de la cancha
    year = strftime("%Y")
    driver.find_element(
        By.XPATH, f"//h4[@data-date='{year}-{cancha_month}-{cancha_day}']").click()
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

    # Rellenar campos especificos de la cancha de tennis del poli don pepe
    if (cancha_sport == "Tennis") and (poli["name"] == "Don Pepe"):
        rellenar_cantidad_asistentes(driver)
        rellenar_localidades(driver)
        rellenar_barrios(driver)
        rellenar_fechas_nacimiento(driver)
        rellenar_domicilios(driver)
        rellenar_telefonos(driver)

    # Rellenar campos generales para todas las canchas
    rellenar_nombres(driver)
    rellenar_apellidos(driver)
    rellenar_dnis(driver)
    rellenar_emails(driver)

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
