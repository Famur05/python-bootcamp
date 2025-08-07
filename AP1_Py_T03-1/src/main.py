from flask import Flask
from web.route.game_route import game_blueprint
from di.container import Container

app = Flask(__name__)

container = Container()

# Регистрация маршрутов
app.register_blueprint(game_blueprint, url_prefix='/game')

if __name__ == '__main__':
    app.run(debug=True)