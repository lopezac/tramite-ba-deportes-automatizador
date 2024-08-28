# tramite-ba-futbol

Hola, este script lo cree para ahorrar tiempo, para automatizar un tramite que cuando lo tenia que hacer era bastante tedioso.

Se pregunta al usuario el link de la pagina de las canchas de futbol en el polideportivo deseado [ejemplo](https://buenosaires.gob.ar/desarrolloeconomico/deportes/futbol-en-el-polideportivo-parque-patricios), luego que tamaño de cancha desea, futbol 5 o 7, la hora y dia (debe chequear de antemano las fechas y horarios disponibles), y el email y contraseña de su cuenta miBA.

Automatizo desde abrir el navegador, con el paquete [Selenium](https://www.selenium.dev/documentation/webdriver/), iniciar sesion, pedir turno, seleccionar horario y fecha, rellenar los datos (nombre, apellido, email y dni), con datos falsos gracias al paquete [Faker](https://github.com/joke2k/faker)

Si tenes errores abriendo el navegador Firefox, y estas en Ubuntu seguramente tengas instalado el navegador con un snap lo que te recomendario seria desintales el navegador y lo instales sin snap.

Aca hay una [guia](https://linuxconfig.org/switching-to-firefoxs-deb-installation-on-ubuntu-22-04-a-guide-to-avoiding-snap-packages) de como desinstalar el Firefox snap e instalarlo como un paquete normal en Ubuntu.

# Instalación

```bash
  # clonamos el repositorio
  git clone https://github.com/lopezac/tramite-ba-futbol.git
  # nos movemos a la carpeta del repositorio clonado
  cd tramite-ba-futbol
  # creamos un python virtual environment
  python3 -m venv .venv
  # entramos al virtual environment
  source .venv/bin/activate
  # instalamos dependencias
  pip3 install -r requirements.txt
  # corremos el programa
  python3 main.py
```
