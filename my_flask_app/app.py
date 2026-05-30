from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Привет, Flask!'

@app.route('/about')
def about():
    return 'О нашем приложении'

# Маршрут с параметром
@app.route('/user/<username>')
def show_user(username):
    return f'Привет, {username}!'

# Маршрут с типизированным параметром
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Это пост номер {post_id}'

# Обработка различных HTTP-методов
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Здесь должна быть логика проверки учетных данных
        return f'Попытка входа: {username}'
    else:
        return 'Пожалуйста, войдите в систему'

# Возврат JSON
@app.route('/api/data')
def get_data():
    data = {
    'name': 'Flask',
    'version': '2.2.3',
    'is_awesome': True
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
