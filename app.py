import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', generated_images=None)

@app.route('/generate', methods=['POST'])
def generate():
    if 'clothing_image' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['clothing_image']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 6 views ke liye mock mapping (jisse upload ki gayi image hi 6 alag boxes mein dikhegi)
        img_url = url_for('static', filename=f'uploads/{filename}')
        six_views = {
            'collar': img_url,
            'pocket': img_url,
            'texture': img_url,
            'sitting': img_url,
            'walking': img_url,
            'studio': img_url
        }
        
        return render_template('index.html', generated_images=six_views)

if __name__ == '__main__':
    app.run(debug=True)
