from flask import Flask, request

class HttpListener:
    def __init__(self, port=8080):
        self.port = port
        self.app = Flask('HttpListener')

    def get_data(self):
        return request.get_json()

    def listen(self, callback, args=()):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'GET':
                try:
                    callback(*args)
                    return '', 204
                except Exception as e:
                    print(e)
                    return 'Bad request', 400
            if request.method == 'POST':
                post_data = request.get_json()
                try:
                    callback(post_data, *args)
                    return '', 204
                except Exception as e:
                    print(e)
                    return 'Bad request', 400

        self.app.run(debug=True,
                     host='127.0.0.1',
                     port=self.port,
                     use_reloader=False)
        
