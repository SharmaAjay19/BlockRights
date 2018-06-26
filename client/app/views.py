import datetime
import json
import uuid
import requests
from flask import render_template, redirect, request

from app import app

vm_config = json.loads(open("../config.txt", "r").read())
# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://" + vm_config["self_ip"] + ":8000"

posts = []

def get_peers():
    response = requests.get("http://13.66.39.222:9000/get_peers")
    nodes = response.json()
    nodelist = [node + ":8000" for node in nodes if node]
    add_node_address = "{}/add_nodes".format(CONNECTED_NODE_ADDRESS)
    requests.post(add_node_address,
                  json=nodelist,
                  headers={'Content-type': 'application/json'})

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content.decode('utf-8'))
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

def fetch_chain():
    """
    Function to fetch the chain from a blockchain node
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
      chain = json.loads(response.content.decode('utf-8'))
      return chain["chain"]
    else:
      return None

@app.route('/')
@app.route('/index')
def index():
    get_peers()
    fetch_posts()
    return render_template('index.html',
                           title='BlockRights: Patent on Blocks',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

@app.route('/visualize')
def visualize():
    #get_peers()
    chain = fetch_chain()
    return render_template('visualization.html',
                           title='BlockRights: Patent on Blocks',
                           node_address=CONNECTED_NODE_ADDRESS,
                           blockchain=chain)

@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    inventors = request.form["inventors"]
    privacy = request.form["privacy"]
    title = request.form["title"]

    post_object = {
        'inventors': inventors,
        'content': post_content,
        'post_id': str(uuid.uuid4()),
        'privacy': privacy,
        'title': title
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
