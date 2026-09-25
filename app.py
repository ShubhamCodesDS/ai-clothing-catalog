import os
import replicate
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Yeh automatically Render ya aapke computer ke Environment Variable se token utha lega
# (Local testing ke liye aap terminal me export kar sakte hain, ya Render dashboard me add karenge)

@app.route('/', methods=['GET', 'POST'])
def index():
    views = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            uploaded_image_url = url_for('static', filename=f'uploads/{filename}')
            
            views = [
                {'title': '1. Collar & Back View', 'url': uploaded_image_url},
                {'title': '2. Pocket & Button View', 'url': uploaded_image_url},
                {'title': '3. Fabric Texture Close-up', 'url': uploaded_image_url},
                {'title': '4. Model Sitting View', 'url': uploaded_image_url},
                {'title': '5. Model Walking View', 'url': uploaded_image_url},
                {'title': '6. Studio Portrait View', 'url': uploaded_image_url}
            ]
            
    return render_template('index.html', views=views)

if __name__ == '__main__':
    app.run(debug=True)
