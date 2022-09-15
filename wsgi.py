from os import environ
from project.app import create_app

app = create_app()

if __name__ == '__main__':
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    create_app().run(port=PORT)
