from faker import Faker
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

people_data = []
people_idx = 0
fake = Faker(["es_AR"])

def read_data(file_location):
    file = open(file_location, 'r')
    lines = file.readlines()
    for line in lines:
        line_data = line.split(',')
        if (len(line_data) != 4): return
        people_data.append({
            "first_name": line_data[0],
            "last_name": line_data[1],
            "email": line_data[2],
            "dni": line_data[3],
        })

def get_person_trait(trait):
    if (len(people_data) > people_idx):
        return people_data[people_idx][trait]
    if (trait == "first_name"):
        return fake.first_name()
    elif (trait == "last_name"):
        return fake.last_name()
    elif (trait == "email"):
        return fake.ascii_free_email()

def get_random_dni():
    return randint(10000000, 47000000)

def main():
    polideportivo_url = "https://buenosaires.gob.ar/desarrolloeconomico/deportes/futbol-en-el-polideportivo-parque-patricios"
    file_location = input("Ingresar direccion de archivo de texto con datos de personas (opcional): ")
    field_day = input("Ingresar dia de reserva de la cancha, ej: 5, 11: ")
    field_hour = input("Ingresar hora de reserva de la cancha, ej: 15, 9: ")
    field_size = input("Ingresar tamaño de la cancha, elegir 5 o 7: ")
    user_email = input("Ingresar correo electronico de la pagina Buenos Aires: ")
    user_password = input("Ingresar contraseña de la pagina Buenos Aires: ")
    if (file_location.endswith(".txt")):
        read_data(file_location)

    driver = webdriver.Firefox()
    driver.get(polideportivo_url)
    driver.find_element(By.PARTIAL_LINK_TEXT, f"fútbol {field_size}").click()
    sleep(10)
    driver.find_element(By.ID, "zocial-mail").click()
    sleep(5)
    driver.find_element(By.ID, "email").send_keys(user_email)
    driver.find_element(By.ID, "password-text-field").send_keys(user_password)
    driver.find_element(By.ID, "login").click()
    sleep(5)
    driver.find_element(By.CLASS_NAME, "btn.btn-default.color-fecha").click()
    sleep(5)
    driver.find_element(By.XPATH, f"//td[text()={field_day}]").click()
    sleep(5)
    driver.find_element(By.XPATH, f"//div[text()='{field_hour}:00 hs.']").click()
    sleep(10)
    driver.find_element(By.CLASS_NAME, "siguiente").click()
    sleep(10)
    assistant_divs = driver.find_elements(By.CLASS_NAME, "panel-body")
    for assistant_div in assistant_divs:
        driver.find_element(By.ID, "form_NombreAlReq").sendkeys(get_person_trait("first_name"))
        driver.find_element(By.ID, "form_ApellidoA1Req").sendkeys(get_person_trait("last_name"))
        driver.find_element(By.ID, "form_EmailA1Req").sendkeys(get_person_trait("email"))
        driver.find_element(By.ID, "form_TipoyNroDocA1Req_numDoc").sendkeys(get_random_dni())
        people_idx += 1
    driver.find_element(By.CLASS_NAME, "siguiente").click()
    sleep(10)
    # driver.find_element(By.CLASS_NAME, "finalizar").click()
    # driver.find_

if __name__ == "__main__":
    main()
