import os
import replicate
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            
            # Local uploaded image URL (jo server par save hui hai)
            uploaded_image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
            
            try:
                # Replicate IDM-VTON model call for Virtual Try-On
                # Yeh model aapki upload ki hui shirt ko ek default model image par fit kar dega
                input_data = {
                    "garm_img": uploaded_image_url,
                    "human_img": "https://raw.githubusercontent.com/yisol/IDM-VTON/main/example/human/example_1.png",
                    "garment_des": "shirt",
                    "category": "upper_body",
                    "is_checked": True,
                    "is_checked_crop": False,
                    "densepose_check": True,
                    "steps": 30,
                }
                
                # Replicate API execution
                output = replicate.run(
                    "cuuupid/idm-vton:c871bb9b046602e353ba0956976d15074d0efd5439f29a2b53b8296d63042453",
                    input=input_data
                )
                
                # Agar API successful rahi, toh generated image URL milega
                generated_image = output if output else uploaded_image_url
                
            except Exception as e:
                print(f"AI Generation Error: {e}")
                generated_image = uploaded_image_url # Fallback agar API mein koi error aaye
            
            # 6 catalog grid views mein AI generated image map ho jayegi
            views = [
                {'title': '1. Collar & Back View', 'url': generated_image},
                {'title': '2. Pocket & Button View', 'url': generated_image},
                {'title': '3. Fabric Texture Close-up', 'url': generated_image},
                {'title': '4. Model Sitting View', 'url': generated_image},
                {'title': '5. Model Walking View', 'url': generated_image},
                {'title': '6. Studio Portrait View', 'url': generated_image}
            ]
            
    return render_template('index.html', views=views)

if __name__ == '__main__':
    app.run(debug=True)
