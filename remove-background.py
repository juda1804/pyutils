import sys
import os
from rembg import remove
from PIL import Image
import numpy as np


def remove_background(input_path, output_path):
    # Cargar la imagen de entrada
    input_image = Image.open(input_path).convert("RGBA")

    # Remover el fondo
    output_data = remove(input_image)

    # Convertir la salida a una matriz numpy si es necesario
    if not isinstance(output_data, np.ndarray):
        output_data = np.array(output_data)

    # Convertir la imagen resultante en un objeto PIL
    output_image = Image.fromarray(output_data).convert("RGBA")

    # Guardar la imagen de salida con alta calidad
    output_image.save(output_path, format='PNG')


def process_images(image_paths, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_path in image_paths:
        # Obtener el nombre y la extensión de la imagen
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)

        # Crear el nuevo nombre con 'r' concatenada antes de la extensión
        new_name = f"{name}r{ext}"

        # Crear la ruta completa para la imagen de salida
        output_path = os.path.join(output_dir, new_name)

        # Remover el fondo de la imagen
        remove_background(image_path, output_path)
        print(f"Procesada: {image_path} -> {output_path}")

if __name__ == "__main__":
    # Lista de rutas de las imágenes a procesar
    image_paths = [
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0626.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0627.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0628.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0629.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0630.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0631.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0632.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0633.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0634.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0635.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0636.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0637.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0638.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0639.JPEG",
        "/home/juan-cadavid/Documents/art-monia/studio/IMG_0640.JPEG",
    ]

    # Directorio donde se guardarán las imágenes sin fondo
    output_dir = 'rm-bg/'

    # Procesar las imágenes
    process_images(image_paths, output_dir)