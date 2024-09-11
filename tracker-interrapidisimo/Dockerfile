# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para Firefox y geckodriver
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    curl \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libgconf-2-4 \
    && rm -rf /var/lib/apt/lists/*


# Descargar e instalar geckodriver
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4) && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

# Instalar Firefox directamente desde los repositorios

RUN apt-get update && apt-get install -y firefox-esr
# Copiar los archivos de requisitos a la imagen
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al contenedor
COPY . /app/

# Exponer el puerto en el que corre el servicio (modifícalo según sea necesario)
EXPOSE 5002

# Establecer variables de entorno para que Selenium funcione en modo sin cabeza (headless)
ENV DISPLAY=:99

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]