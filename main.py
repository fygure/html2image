import json
from jinja2 import Environment, FileSystemLoader
from html2image import Html2Image
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Configuration
json_file = 'data.json'          # Path to your JSON file
template_file = 'template.html'  # HTML template file
output_image = 'output.png'      # Output image file name
output_dir = 'output'            # Directory to save the output image

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load JSON data
try:
    with open(json_file, 'r') as f:
        data = json.load(f)
    logging.info(f"Loaded data from {json_file}")
except FileNotFoundError:
    logging.error(f"JSON file '{json_file}' not found.")
    exit(1)
except json.JSONDecodeError as e:
    logging.error(f"Error decoding JSON: {e}")
    exit(1)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
try:
    template = env.get_template(template_file)
    logging.info(f"Loaded template '{template_file}'")
except Exception as e:
    logging.error(f"Error loading template: {e}")
    exit(1)

# Render HTML with data
html_content = template.render(data=data)

# Initialize Html2Image
hti = Html2Image(output_path=output_dir)

# Optionally, specify Chromium path if not in PATH
# hti = Html2Image(chromium_path='C:/Path/To/Chromium/chrome.exe', output_path=output_dir)

# Render the HTML to an image with an empty css_str
try:
    hti.screenshot(
        html_str=html_content,
        css_str=[],               # Pass an empty list instead of None
        save_as=output_image,
        size=(1000, 800)           # Adjusted size for better layout
    )
    logging.info(f"Image saved as {os.path.join(output_dir, output_image)}")
except Exception as e:
    logging.error(f"Error generating image: {e}")
    exit(1)
