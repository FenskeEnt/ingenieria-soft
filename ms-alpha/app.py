from main import create_app, db
import time

app = create_app()

app.app_context().push()

@app.route('/healthcheck')
def healthcheck():
    return 'App working correctly!', 200

@app.route('/compras')
def compras():
    time.sleep(3)
    compras = [
        {
            'id': 1,
            'nombre': 'Arroz',
            'cantidad': 1,
            'precio': 2.50
        },
        {
            'id': 2,
            'nombre': 'Leche',
            'cantidad': 2,
            'precio': 1.50
        },
        {
            'id': 3,
            'nombre': 'Papa',
            'cantidad': 3,
            'precio': 0.50
        }
    ]
    return compras, 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)