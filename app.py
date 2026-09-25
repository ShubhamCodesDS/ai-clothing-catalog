import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Upload folder aur allowed extensions
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_catalog_views(input_image_path, filename):
    """
    Yeh function user ki uploaded shirt ko process karke 
    alag-alag views generate karega.
    """
    try:
        base_img = Image.open(input_image_path).convert("RGB")
    except Exception:
        return None

    views = []
    view_names = [
        ("Collar & Brand Tag View", "collar"),
        ("Pocket & Button View", "pocket"),
        ("Fabric Texture Close-up", "texture"),
        ("Model Sitting View", "sitting"),
        ("Model Walking View", "walking"),
        ("Studio Portrait View", "portrait")
    ]

    for title, vtype in view_names:
        # Har view ke liye ek custom processed variant banate hain
        output_filename = f"{vtype}_{filename}"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        # Simple simulation/processing: User ki image ko alag tarike se crop/resize karke show karna
        width, height = base_img.size
        if vtype == "collar":
            box = (int(width*0.25), 0, int(width*0.75), int(height*0.5))
        elif vtype == "pocket":
            box = (int(width*0.3), int(width*0.3), int(width*0.8), int(height*0.8))
        elif vtype == "texture":
            box = (int(width*0.4), int(height*0.4), int(width*0.7), int(height*0.7))
        else:
            box = (0, 0, width, height)
            
        cropped_img = base_img.crop(box) if vtype in ["collar", "pocket", "texture"] else base_img
        # Resize standard professional view dimensions
        cropped_img = cropped_img.resize((600, 600))
        cropped_img.save(output_path)
        
        views.append({
            'title': title,
            'url': url_for('static', filename=f'processed/{output_filename}')
        })
        
    return views

@app.route('/', methods=['GET', 'POST'])
def index():
    views = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Generate views for the uploaded shirt
            views = generate_catalog_views(input_path, filename)
            
    return render_template('index.html', views=views)

if __name__ == '__main__':
    app.run(debug=True)
