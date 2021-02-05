"""Application entry point."""
from chickenflask import init_app


app = init_app()


if __name__ == '__main__':
    app.run(host='192.168.0.129')

