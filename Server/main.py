from MyHandler import MyHandler
import helpers.DynamoDB as db
from http.server import HTTPServer
from pyngrok import ngrok

PORT_NUMBER = 8080
ngrok_path = "/usr/bin/ngrok"	# NGROK PATH

# GET URL WITHOUT PYNGROK
# def start_ngrok():
#	r = requests.get( "http://localhost:4040/api/tunnels")
#  	data = r.json()
#	return data["tunnels"][1]["public_url"]
def start_ngrok():
    print("Starting ngrok")
    url = ngrok.connect(port=8080, ngrok_path=ngrok_path)
    return url


if __name__ == '__main__':
    try:
        public_url = start_ngrok()
        db.write_url(public_url)
        print(f"{public_url} write on DynamoDB")
        server = HTTPServer(('', PORT_NUMBER), MyHandler)
        print('Server started on port:{}'.format(PORT_NUMBER))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()
        ngrok.kill(ngrok_path=ngrok_path)
