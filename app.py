from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Multi-shirt database using your exact GitHub static filenames
SHIRTS_DATABASE = {
    'blue_stripe': {
        'name': 'Classic Blue Stripe Shirt',
        'views': [
            {'title': '1. Collar & Brand Tag View', 'url': 'sample_collar.jpg'},
            {'title': '2. Pocket & Button View', 'url': 'sample_pocket.jpg'},
            {'title': '3. Fabric Texture Close-up', 'url': 'sample_texture.jpg'},
            {'title': '4. Model Sitting View', 'url': 'sample_sitting.jpg'},
            {'title': '5. Model Walking View', 'url': 'sample_walking.jpg'},
            {'title': '6. Studio Portrait View', 'url': 'sample_portrait.jpg'}
        ]
    },
    'checked_shirt': {
        'name': 'Checkered Plaid Shirt',
        'views': [
            {'title': '1. Collar & Brand Tag View', 'url': 'sample_collar.jpg'},
            {'title': '2. Pocket & Button View', 'url': 'sample_pocket.jpg'},
            {'title': '3. Fabric Texture Close-up', 'url': 'sample_texture.jpg'},
            {'title': '4. Model Sitting View', 'url': 'sample_sitting.jpg'},
            {'title': '5. Model Walking View', 'url': 'sample_walking.jpg'},
            {'title': '6. Studio Portrait View', 'url': 'sample_portrait.jpg'}
        ]
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_shirt_key = 'blue_stripe'
    
    if request.method == 'POST':
        selected_shirt_key = request.form.get('shirt_choice', 'blue_stripe')
    
    shirt_data = SHIRTS_DATABASE.get(selected_shirt_key, SHIRTS_DATABASE['blue_stripe'])
    
    formatted_views = []
    for view in shirt_data['views']:
        formatted_views.append({
            'title': view['title'],
            'url': url_for('static', filename=view['url'])
        })
        
    return render_template('index.html', views=formatted_views, current_shirt=selected_shirt_key)

if __name__ == '__main__':
    app.run(debug=True)
