from main import create_app, db, cache
import os, requests

app = create_app()

app.app_context().push()

@app.route('/healthcheck')
def healthcheck():
    return 'App working correctly!', 200

@app.route('/show-compras', methods=['GET'])
@cache.cached(timeout=600)
def show_compras():
    url_compras = os.getenv('URL_MS_ALPHA')
    compras = requests.get(f'{url_compras}/compras', verify=False).json()
    return compras, 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=7000, debug=True)