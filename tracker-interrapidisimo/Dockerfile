# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos a la imagen
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al contenedor
COPY . /app/

# Exponer el puerto en el que corre el servicio (modifícalo según sea necesario)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]