import json
from flask import Flask, request

app = Flask(__name__)
try:
	peerfile = open("peerlist.txt", "r+")
	peerlist = set([x.strip() for x in peerfile.readlines()])
except Exception as e:
	peerlist = set()

@app.route('/get_peers', methods=['GET'])
def get_peers():
	ip = request.remote_addr
	if not ip:
		return "Invalid user", 404
	resultlist = list(peerlist)
	try:
		resultlist.remove(ip)
	except Exception as e:
		a = 1
	peerlist.add(ip)
	peerfile = open("peerlist.txt", "w+")
	peerfile.write('\n'.join(list(peerlist)))
	peerfile.close()
	return json.dumps(resultlist), 201

app.run(host="0.0.0.0", port=9000)