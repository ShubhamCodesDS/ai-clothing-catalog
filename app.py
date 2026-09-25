import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
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
            
            # Yahan hum fix ki jagah user ki upload ki gayi image ka path use kar rahe hain
            uploaded_image_url = url_for('static', filename=f'uploads/{filename}')
            
            generated_views = [
                {'title': '1. Collar & Brand Tag View', 'url': uploaded_image_url},
                {'title': '2. Pocket & Button View', 'url': uploaded_image_url},
                {'title': '3. Fabric Texture Close-up', 'url': uploaded_image_url},
                {'title': '4. Model Sitting View', 'url': uploaded_image_url},
                {'title': '5. Model Walking View', 'url': uploaded_image_url},
                {'title': '6. Studio Portrait View', 'url': uploaded_image_url}
            ]
            
            return render_template('index.html', views=generated_views, uploaded_image=uploaded_image_url)
            
    return render_template('index.html', views=None)

if __name__ == '__main__':
    app.run(debug=True)
