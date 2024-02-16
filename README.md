# tramite-ba-futbol

Hola, este script lo cree para ahorrar tiempo, para automatizar un tramite 
que cuando lo tenia que hacer era bastante tedioso.

Se pregunta al usuario el link de la pagina de las canchas de futbol en el polideportivo 
deseado [ejemplo](https://buenosaires.gob.ar/desarrolloeconomico/deportes/futbol-en-el-polideportivo-parque-patricios), 
luego que tamaño de cancha desea, futbol 5 o 7, la hora y dia (debe chequear de antemano las 
fechas y horarios disponibles), y el email y contraseña de su cuenta miBA.

Automatizo desde abrir el navegador, con el paquete [Selenium](https://www.selenium.dev/documentation/webdriver/), 
iniciar sesion, pedir turno, seleccionar horario y fecha, rellenar los datos 
(nombre, apellido, email y dni), con datos falsos gracias al paquete 
[Faker](https://github.com/joke2k/faker)

# Instalación

```bash
  # clonar repositorio
  git clone git@github.com:lopezac/tramite-ba-futbol.git
  # instalar dependencias
  pip install -r requirements.txt
  # correr programa
  python3 main.py
```
