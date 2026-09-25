import os
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Multiple shirts database with their professional high-end views mapped properly
SHIRTS_DATABASE = {
    'blue_stripe': {
        'name': 'Classic Blue Stripe Shirt',
        'views': [
            {'title': '1. Collar & Brand Tag View', 'url': 'sample_collar_2.jpg'},
            {'title': '2. Pocket & Button View', 'url': 'sample_pocket_2.jpg'},
            {'title': '3. Fabric Texture Close-up', 'url': 'sample_texture_2.jpg'},
            {'title': '4. Model Sitting View', 'url': 'sample_sitting_2.jpg'},
            {'title': '5. Model Walking View', 'url': 'sample_walking_2.jpg'},
            {'title': '6. Studio Portrait View', 'url': 'sample_portrait_2.jpg'}
        ]
    },
    'checked_shirt': {
        'name': 'Checkered Plaid Shirt',
        'views': [
            {'title': '1. Collar & Brand Tag View', 'url': '2.png'},
            {'title': '2. Pocket & Button View', 'url': '2.png'},
            {'title': '3. Fabric Texture Close-up', 'url': '2.png'},
            {'title': '4. Model Sitting View', 'url': '2.png'},
            {'title': '5. Model Walking View', 'url': '2.png'},
            {'title': '6. Studio Portrait View', 'url': '2.png'}
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
