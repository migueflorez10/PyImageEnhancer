import os
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor
import time

def create_preview(original, enhanced):
    width, height = original.size
    new_image = Image.new('RGB', (width * 2, height))
    new_image.paste(original, (0, 0))
    new_image.paste(enhanced, (width, 0))
    return new_image

def adjust_image(image_path, output_path, preview_path, brightness_factor, contrast_factor, color_factor, log_file):
    start_time = time.time()

    with Image.open(image_path) as img:
        original = img.copy()
        img = ImageEnhance.Brightness(img).enhance(brightness_factor)
        img = ImageEnhance.Contrast(img).enhance(contrast_factor)
        img = ImageEnhance.Color(img).enhance(color_factor)
        img.save(output_path)

        
        preview = create_preview(original, img)
        preview.save(preview_path)

    end_time = time.time()
    processing_time = end_time - start_time

    with open(log_file, "a") as log:
        log.write(f"{image_path}, {processing_time:.2f} sec, Brillo: {brightness_factor}, Contraste: {contrast_factor}, Color: {color_factor}\n")

    print(f"Tiempo de procesamiento para {image_path}: {processing_time:.2f} segundos")

def process_images_concurrently(image_folder, output_folder, preview_folder, brightness_factor, contrast_factor, color_factor, log_file):
    with ThreadPoolExecutor() as executor:
        for image_file in os.listdir(image_folder):
            if image_file.endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(image_folder, image_file)
                output_path = os.path.join(output_folder, image_file)
                preview_path = os.path.join(preview_folder, f"preview_{image_file}")
                executor.submit(adjust_image, image_path, output_path, preview_path, brightness_factor, contrast_factor, color_factor, log_file)

if __name__ == "__main__":
    input_folder = "input_images"
    output_folder = "enhanced_images"
    preview_folder = "previews"
    log_file = "image_processing_log.txt"
    brightness_factor = 1.2
    contrast_factor = 1.2
    color_factor = 1.2

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(preview_folder, exist_ok=True)

    open(log_file, 'w').close()

    start_time = time.time()
    process_images_concurrently(input_folder, output_folder, preview_folder, brightness_factor, contrast_factor, color_factor, log_file)
    end_time = time.time()

    print(f"Tiempo total de procesamiento: {end_time - start_time} segundos")
