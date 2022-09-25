from website import create_app
from werkzeug.exceptions import HTTPException
from flask import render_template


app = create_app()


# general error handeler
@app.errorhandler(HTTPException)
def handle_exception(e):
    # generate response
    response = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }

    return render_template(
        'error.html',
        response=response
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
