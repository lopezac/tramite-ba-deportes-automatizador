from faker import Faker
from random import randint
from selenium import webdriver

people_data = []
people_idx = 0
fake = Faker(["es_AR"])

def read_data(file_location):
    if (not file_location.endswith(".txt")):
        return
    file = open(file_location, 'r')
    lines = file.readlines()
    for line in lines:
        line_data = line.split(',')
        if (strlen(line_data) == 4):
            people_data.push({
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
# function main()
#   prompt user for direction of people_data text file, save at file_location 
#   prompt user for number dia de reserva ej : 5, 6, 9, store field_day
#   prompt user for number hour ej: 14, 9, 15, store field_hour
#   prompt user for number field size: 5, 7, store in field_size
#   prompt user for string email, store in email
#   prompt user for string password, store in password
#   if file_location is not null
#     read_data(file_location)
#   open web browser
#   go to cancha reserva page parque patricios url
#   wait 5 seconds
#   click reserve cancha size field_size
#   wait 5 seconds
#   click ingresar con email
#   select and type variable email at email input
#   select and type variable password at password input
#   select and click ingresar button
#   wait 5 seconds
#   select por fecha card, click comenzar button inside
#   select the day selected field_day and click
#   wait 5 seconds
#   click text containing field_hour, click
#   wait 5 seconds
#   select and click siguiente button
#   wait 5 seconds
#   select father content of "datos de los asistentes", store in assistant_divs
#   loop children assistant_divs, each children called assistant_div
#     select input text nombre, store assistant_name
#     set assistant_name to get_person_trait("first_name")
#     select input text apellido, store assistant_lastname
#     set assistant_lastname to get_person_trait("last_name")
#     select input text email, store assistant_email
#     set assistant_email to get_person_trait("email")
#     select input text dni, store assistant_dni
#     set assistant_dni to get_person_trait("dni")
#     increase people_idx by 1
#   select button with "siguiente" text, click it
#   wait 5 seconds
#   select button with "finalizar" text, click it

# fake = Faker(["es_AR"])
# person = { 
#     "first_name": "Axel", 
#     "last_name": "Lopez",
#     "email": "lopezaxel@protonmail.com",
#     "dni": "46441225"
# }
# print("person[\"first_name\"]", person["first_name"])
# trait = "first_name"
# print(fake.first_name())
# print(fake.last_name())
# print(fake.ascii_free_email())
# print(randint(10000000, 47000000))
#
# driver = webdriver.Firefox()
# driver.get("https://www.google.com")
# driver.close()
