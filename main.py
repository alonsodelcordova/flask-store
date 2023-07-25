from apps import init_app
from apps.errors import not_found, error_server

app = init_app()


if __name__ == '__main__':
    app.run(debug=True)

