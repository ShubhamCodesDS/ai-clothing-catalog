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
            
            # Yahan hum 6 professional catalog views ke paths set kar rahe hain
            # Aap inhe apne static folder ki real images se replace kar sakte hain
            generated_views = [
                {'title': '1. Collar & Brand Tag View', 'url': url_for('static', filename='sample_collar.jpg')},
                {'title': '2. Pocket & Button View', 'url': url_for('static', filename='sample_pocket.jpg')},
                {'title': '3. Fabric Texture Close-up', 'url': url_for('static', filename='sample_texture.jpg')},
                {'title': '4. Model Sitting View', 'url': url_for('static', filename='sample_sitting.jpg')},
                {'title': '5. Model Walking View', 'url': url_for('static', filename='sample_walking.jpg')},
                {'title': '6. Studio Portrait View', 'url': url_for('static', filename='sample_portrait.jpg')}
            ]
            
            return render_template('index.html', views=generated_views, uploaded_image=url_for('static', filename=f'uploads/{filename}'))
            
    return render_template('index.html', views=None)

if __name__ == '__main__':
    app.run(debug=True)
