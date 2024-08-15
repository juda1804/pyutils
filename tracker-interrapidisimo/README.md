Para obtener la ruta de chromedriver en Ubuntu, puedes seguir estos pasos:

1. Descargar chromedriver
Primero, descarga chromedriver desde el sitio oficial, asegurándote de que la versión coincida con la de tu navegador Chrome:

bash
Copy code
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
Descomprime el archivo descargado:

bash
Copy code
unzip chromedriver_linux64.zip
2. Mover chromedriver a un directorio en el PATH
Para que chromedriver esté disponible globalmente en tu sistema, puedes moverlo a /usr/local/bin, que es un directorio comúnmente incluido en el PATH:

bash
Copy code
sudo mv chromedriver /usr/local/bin/
3. Verificar la ruta
Para verificar que chromedriver está correctamente instalado y obtener su ruta, puedes ejecutar:

bash
Copy code
which chromedriver
Este comando te mostrará la ruta completa de chromedriver, que debería ser algo como:

bash
Copy code
/usr/local/bin/chromedriver
Uso en Python
Una vez que tengas la ruta, puedes usarla en tu código de Python como:

python
Copy code
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
Con esto, Selenium podrá utilizar chromedriver para automatizar las acciones en el navegador Chrome en tu sistema Ubuntu.