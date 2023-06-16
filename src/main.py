from reactpy import component, html
from reactpy.backend.fastapi import configure, FastAPI

@component
def HelloWorld():
    return html.div(
        html.h1("Hello, world!")
    )


app = FastAPI()
configure(app, HelloWorld)

# if __name__ == '__main__':

