from wsgiref.simple_server import make_server

def run_webapp(host, port, app):
    try:
        
        server = make_server(host, port, app)
        print(f"Server running on 'http://{host}:{port}/', Press Ctrl-C to stop.")
        server.serve_forever()
    except KeyboardInterrupt: pass