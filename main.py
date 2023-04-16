from faker import Faker
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep

fake = Faker(["es_AR"])

def get_person_trait(trait):
    if (trait == "first_name"):
        return fake.first_name()
    elif (trait == "last_name"):
        return fake.last_name()
    elif (trait == "email"):
        return fake.ascii_free_email()

def get_random_dni():
    return randint(10000000, 47000000)

def main():
    polideportivo_url = input(
        "Ingresar URL de la pagina de las canchas del polideportivo deseado, (vacio Parque Patricios Futbol): "
    )
    if len(polideportivo_url) < 20:
        polideportivo_url = "https://buenosaires.gob.ar/desarrolloeconomico/deportes/futbol-en-el-polideportivo-parque-patricios"
    field_day = input("Ingresar dia de reserva de la cancha, (ejemplo: 4, 11): ")
    field_hour = input("Ingresar la hora de reserva de la cancha, (ejemplo: 14, 09): ")
    field_size = input("Ingresar el tamaño de la cancha, elegir 5 o 7: ")
    field_type = input("Ingresar el tipo de cancha, elegir asfalto o sintetico: ")
    user_email = input("Ingresar el email de tu cuenta miBA: ")
    user_password = input("Ingresar la contraseña de tu cuenta miBA: ")

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get(polideportivo_url)
    driver.find_element(By.PARTIAL_LINK_TEXT, f"fútbol {field_size}").click()
    sleep(10)
    driver.find_element(By.ID, "zocial-mail").click()
    sleep(4)
    driver.find_element(By.ID, "email").send_keys(user_email)
    driver.find_element(By.ID, "password-text-field").send_keys(user_password)
    driver.find_element(By.ID, "login").click()
    sleep(4)
    driver.find_element(By.CLASS_NAME, "btn.btn-default.color-fecha").click()
    sleep(4)
    driver.find_element(By.XPATH, f"//td[text()={field_day}]").click()
    sleep(4)
    driver.find_element(By.XPATH, f"//td[text()={field_type}]").click();
    sleep(4)
    driver.find_element(By.XPATH, f"//div[text()='{field_hour}:00 hs.']").click()
    sleep(4)
    driver.find_element(By.CLASS_NAME, "siguiente").click()
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

    driver.find_element(By.CLASS_NAME, "siguiente").click()
    driver.find_element(By.ID, "confirmarTurno").click()
    sleep(4)
    driver.find_element(By.CLASS_NAME, "siguiente").click()

if __name__ == "__main__":
    main()
