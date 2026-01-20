from flask import Flask, request, render_template, send_from_directory
import fitz
from PIL import Image
from io import BytesIO
import os
import webbrowser

# Changer le répertoire de travail au répertoire du script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    pdf_file = request.files['pdfFile']  # Modification ici : 'pdfFile' au lieu de 'pdf_file'
    pdf_file_path = os.path.join('templates/static', pdf_file.filename)
    pdf_file.save(pdf_file_path)

    output_folder = "templates/static"
    image_paths = convert_pdf_to_jpg(pdf_file_path, output_folder)
    return render_template('result.html', image_paths=image_paths)

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory('templates/static', filename, as_attachment=True)

def convert_pdf_to_jpg(pdf_file, output_folder):
    pdf_document = fitz.open(pdf_file)
    
    pdf_file_name = os.path.splitext(os.path.basename(pdf_file))[0]
    image_paths = []  # Liste pour stocker les chemins des fichiers images

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            base_image = pdf_document.extract_image(img[0])
            image_data = base_image["image"]
            image_bytes = BytesIO(image_data)
            image = Image.open(image_bytes)
            
            image_path = f"{pdf_file_name}_page_{page_number + 1}_image_{img_index + 1}.jpg"
            image_paths.append(image_path)  # Ajouter le chemin à la liste

            image.save(os.path.join(output_folder, image_path), "JPEG")
            print(f"Image saved: {image_path}")
    
    pdf_document.close()
    return image_paths

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')

    app.run(debug=True)

