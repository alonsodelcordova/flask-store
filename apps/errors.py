from apps import app

@app.errorhandler(404)
def not_found(error):
    return {
        'code': 404,
        'mesage': 'Ruta no existe'
    }, 404


@app.errorhandler(500)
def error_server(error):
    return {
        'code': 500,
        'mesage': 'Error interno'
    }, 500

