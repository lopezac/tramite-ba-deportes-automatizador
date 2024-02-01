from faker import Faker
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

fake = Faker(["es_AR"])

polis = [
    { name: "Parque Patricios", canchas: [5, 7], url:"" },
    { name: "Costa Rica", canchas: [5], url:"https://buenosaires.gob.ar/desarrolloeconomico/deportes/actividades/futbol-5-en-el-polideportivo-costa-rica" },
    { name: "Santojanni", canchas: [5, 9], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-santojanni" },
    { name: "Avellaneda", canchas: [7, 9, 11], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-avellaneda" },
    { name: "Colegiales", canchas: [5], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-colegiales" },
    { name: "Don Pepe", canchas: [5], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-don-pepe" },
    { name: "Dorrego", canchas: [5], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-dorrego" },
    { name: "Martin Fierro", canchas: [5, 7], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-martin-fierro" },
    { name: "Onega", canchas: [5], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-onega" },
    { name: "Pereyra", canchas: [5, 7], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-pereyra" },
    { name: "Pomar", canchas: [9], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-pomar" },
    { name: "Sarmiento", canchas: [5], url:"https://buenosaires.gob.ar/jefaturadegabinete/deportes/futbol-en-el-polideportivo-sarmiento" },
]

supported_browsers = [
    { name: "Firefox" }, { name: "chrome" }
]

def get_person_trait(trait):
    if (trait == "first_name"):
        return fake.first_name()
    elif (trait == "last_name"):
        return fake.last_name()
    elif (trait == "email"):
        return fake.ascii_free_email()

def get_random_dni():
    return randint(10000000, 47000000)

def get_poli_url():
    for i in enumerate(polis):
        print(f"{i} - Polideportivo {polis[i].name}")
    poli_idx = input("Ingrese el numero del polideportivo deseado: ")
    return polis[poli_idx]

def get_cancha_size(poli_idx):
    canchas = polis[poli_idx].canchas
    for i in enumerate(canchas):
        print("f{i} - Cancha futbol {canchas[i]}")
    cancha_idx = input("Ingrese el numero de la cancha deseada: ")
    return canchas[cancha_idx]

def get_browser_name():
    for i in enumerate(supported_browsers):
        print(f"{i} - {supported_browsers[i].name}")
    browser_idx = input("Ingrese el numero del navegador web a utilizar: ")
    return supported_browsers[browser_idx].idx;

def get_browser():
    browser_name = get_browser_name()
    if browser_name == "firefox":
        return webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    elif browser_name == "chrome":
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def main():
    [poli_url, poli_idx] = get_poli_url()
    cancha_day = input("Ingresar dia de reserva de la cancha: ")
    cancha_hour = input("Ingresar la hora de reserva de la cancha: ")
    cancha_size = get_cancha_size(poli_idx)
    cancha_type = input("Ingresar el tipo de cancha, elegir asfalto o sintetico: ")
    user_email = input("Ingresar el email de tu cuenta miBA: ")
    user_password = input("Ingresar la contraseña de tu cuenta miBA: ")

    driver = get_browser()
    driver.get(poli_url)
    # https://formulario-sigeci.buenosaires.gob.ar/InicioTramite?idPrestacion=
    driver.find_element(By.PARTIAL_LINK_TEXT, "https://formulario-sigeci.buenosaires.gob.ar/InicioTramite?idPrestacion=").click()
    sleep(10)
    driver.find_element(By.ID, "zocial-mail").click()
    sleep(4)
    driver.find_element(By.ID, "email").send_keys(user_email)
    driver.find_element(By.ID, "password-text-field").send_keys(user_password)
    driver.find_element(By.ID, "login").click()
    sleep(4)
    # driver.find_element(By.XPATH, f"//div[@data-start]='fecha'").click()
    driver.find_element(By.XPATH, f"//h4[@data-start]='2024-02-{cancha_day}'").click()
    sleep(4)
    driver.find_element(By.XPATH, f"//input[@data-start]='2024-02-{cancha_day}'").click()
    sleep(4)
    # driver.find_element(By.XPATH, f"//input[text()={cancha_type}]").click();
    # sleep(4)
    driver.find_element(By.ID, "save").click()
    sleep(4)
    driver.find_element(By.XPATH, f"//input[@data-hour]='{cancha_hour}:00 hs.'").click()
    sleep(4)
    driver.find_element(By.ID, "next").click()
    sleep(4)
    nombre_inputs = driver.find_elements(By.XPATH, "//input[contains(@id, 'form_Nombre')]");
    apellido_inputs = driver.find_elements(By.XPATH, "//input[contains(@id, 'form_Apellido')]");
    email_inputs = driver.find_elements(By.XPATH, "//input[contains(@id, 'form_Email')]");
    # strange email with different id form_emailA5REQ
    email_inputs.append(driver.find_element(By.XPATH, "//input[contains(@id, 'form_email')]"))
    dni_inputs = driver.find_elements(By.XPATH, "//input[contains(@id, 'form_TipoyNroDocA')][@type='number']");

    for nombre_input in nombre_inputs:
        nombre_input.send_keys(get_person_trait("first_name"))
    for apellido_input in apellido_inputs:
        apellido_input.send_keys(get_person_trait("last_name"))
    for email_input in email_inputs:
        email_input.send_keys(get_person_trait("email"))
    for dni_input in dni_inputs:
        dni_input.send_keys(get_random_dni())

    driver.find_element(By.ID, "exit").click()
    driver.find_element(By.ID, "confirmarTurno").click()
    sleep(4)
    driver.find_element(By.CLASS_NAME, "siguiente").click()

if __name__ == "__main__":
    main()
