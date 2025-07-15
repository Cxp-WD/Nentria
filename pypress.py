from flask import Flask, send_from_directory, Response, request, jsonify
import subprocess, os

def Server(name="Unnamed", folder='www'):
    return Flask(__name__, static_folder=folder)

def launch(server, port=8080):
    server.run(host='0.0.0.0', port=port)

class api():
    def host(app, path='/api/', requests=['GET', 'POST'], get=None, post=None, success_message='Ok'):
        @app.route(path, methods=requests)
        def serve_api():
            if request.method == 'POST':
                post(request.get_json())
                return success_message, 200
            elif request.method == 'GET':
                return get(request.get_json())
            else:
                return "Invalid request", 400

class webserver():
    def host(app ,folder='www'):
        @app.route('/')
        def serve_index():
            index_php_path = os.path.join(app.static_folder, 'index.php')
            index_html_path = os.path.join(app.static_folder, 'index.html')

            if os.path.exists(index_html_path):
                return send_from_directory(app.static_folder, 'index.html')

            return "No index file found", 404

        @app.route('/<path:filename>')
        def serve_static_files(filename):
            if filename.endswith('.php'):
                php_file_path = os.path.join(app.static_folder, filename)
                if os.path.exists(php_file_path):
                    result = subprocess.run(['php', php_file_path], capture_output=True, text=True)
                    return Response(result.stdout, content_type='text/html')
                else:
                    return "File not found", 404
            return send_from_directory(app.static_folder, filename)
