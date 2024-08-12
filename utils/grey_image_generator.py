import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import inflect
import logging
import csv

# Setup logging to capture errors
logging.basicConfig(filename="image_generation_errors.log", level=logging.ERROR)

# Function to generate words
p = inflect.engine()

def get_number_word(number):
    word = p.number_to_words(number)
    words = word.replace('-', ' ').split()
    lower_words = [''.join(word.lower()) for word in words]
    lower_word = ' '.join(lower_words)
    upper_words = [''.join(word.upper()) for word in words]
    upper_word = ' '.join(upper_words)
    title_words = [''.join(word.title()) for word in words]
    title_word = ' '.join(title_words)
    if number == 100:
        lower_word, upper_word, title_word = lower_words[1], upper_words[1], title_words[1]
    
    word_list = [lower_word, upper_word, title_word]
    return word_list

# Generating the list of words for numbers from 1 to 100
words_dict = {i: get_number_word(i) for i in range(1, 101)}

# Path to the fonts directory
fonts_directory = r"D:\Number_recognition_project\Fonts"

# List all font files in the directory
font_files = [f for f in os.listdir(fonts_directory) if f.endswith('.ttf') or f.endswith('.otf')]

# Ensuring that there are fonts available
if not font_files:
    raise FileNotFoundError("No font files found in the specified directory.")

# different font
font_sizes = [i for i in range(10,25,2)]

# Font colors
font_colors = [ (i) for i in range(0,201,10)]

# Function to generate random grayscale background color
def random_gray_value():
    gray_value = random.randint(0, 255)
    return gray_value

# Function to generate random values within a specified range
def random_value(min_val, max_val, apply_effect=True):
    return np.random.uniform(min_val, max_val) if apply_effect else 0

# Creating base directory for images
base_directory = "word_images"
os.makedirs(base_directory, exist_ok=True)

# Creating CSV file to store image filenames and labels
csv_file_path = os.path.join(base_directory, "image_labels.csv")
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["filename", "label"])  # Header row

    total_images = 0
    for number, word_variants in words_dict.items():
        for variant_idx, word in enumerate(word_variants):
            for i in range(200):  # Generate 200 images for each word variant
                try:
                    font_file = random.choice(font_files)
                    font_path = os.path.join(fonts_directory, font_file)

                    font_size = random.choice(font_sizes)
                    font = ImageFont.truetype(font_path, font_size)

                    background_color = random_gray_value()
                    bg_image = Image.new('L', (160,40), color=background_color)
                    draw = ImageDraw.Draw(bg_image)

                    font_color = random.choice(font_colors)

                    apply_rotation = random.choice([True, False])
                    rotation_angle = random_value(-3, 3, apply_rotation)

                    x_pos = random_value(5, 20)
                    y_pos = random_value(5, 20)

                    rotated_text_image = Image.new('L', (160, 40), 255)
                    draw_rotated = ImageDraw.Draw(rotated_text_image)
                    draw_rotated.text((x_pos, y_pos), word, font=font, fill=font_color)
                    rotated_text_image = rotated_text_image.rotate(rotation_angle, resample=Image.BICUBIC, expand=1)

                    bg_width, bg_height = bg_image.size
                    text_width, text_height = rotated_text_image.size
                    x_pos = (bg_image.width - text_width) // 2
                    y_pos = (bg_image.height - text_height) // 2
                    bg_image.paste(rotated_text_image, (x_pos, y_pos), rotated_text_image)

                    apply_blur = random.choice([True, False])  #applying blur
                    blur_radius = random_value(0, 1.5, apply_blur)
                    blurred_image = bg_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

                    apply_noise = random.choice([True, False])  # adding noise
                    noise_scale = random_value(0, 10, apply_noise)

                    if apply_noise:
                        image_array = np.array(blurred_image)
                        noise = np.random.normal(loc=0, scale=noise_scale, size=image_array.shape)
                        noisy_image_array = np.clip(image_array + noise, 0, 255).astype(np.uint8)
                        final_image = Image.fromarray(noisy_image_array)
                    else:
                        final_image = blurred_image

                    # Saving final image with number, variant, and image index included in the filename
                    filename = f'{number}_{variant_idx+1}_{i+1}.png'
                    final_image.save(os.path.join(base_directory, filename))

                    # Writing filename and label to CSV
                    csv_writer.writerow([filename, number])

                    total_images += 1

                except Exception as e:
                    logging.error(f"Failed to generate image for word '{word}' (number {number}), variant {variant_idx+1}, image {i+1}: {str(e)}")

print(f"Images generated successfully! Total images generated: {total_images}")
