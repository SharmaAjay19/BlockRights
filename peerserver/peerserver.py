import json
from flask import Flask, request

app = Flask(__name__)
try:
	peerfile = open("peerlist.txt", "r+")
	peerlist = set(peerfile.readlines())
except Exception as e:
	peerlist = set()

@app.route('/get_peers', methods=['GET'])
def get_peers():
	ip = request.remote_addr
	if not ip:
		return "Invalid user", 404
	peerlist.add(ip)
	peerfile = open("peerlist.txt", "w+")
	peerfile.write('\n'.join(list(peerlist)))
	peerfile.close()
	return json.dumps(list(peerlist)), 201

app.run(host="0.0.0.0", port=9000)