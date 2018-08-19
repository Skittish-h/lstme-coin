from flask import Flask
from blockman import *
import json
from flask import request
node = Flask(__name__)

# Store the transactions that
# this node has in a list

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

print blockchain[0]

this_nodes_transactions = []
@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  # Convert our blocks into dictionaries
  z = []
  # so we can send them as json objects later
  for i in chain_to_send:
    block = chain_to_send[0]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = str(block.hash)
    z[i] = {
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash
    }
  # Send our chain to whomever requested it
  chain_to_send = json.dumps(chain_to_send)
  return chain_to_send

def find_new_chains():
  # Get the blockchains of every
  # other node
  other_chains = []
  for node_url in peer_nodes:
    # Get their chains using a GET request
    block = requests.get(node_url + "/blocks").content
    # Convert the JSON object to a Python dictionary
    block = json.loads(block)
    # Add it to our list
    other_chains.append(block)
  return other_chains

def consensus():
  # Get the blocks from other nodes
  other_chains = find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain wasn't ours,
  # then we set our chain to the longest
  blockchain = longest_chain
@node.route('/txion', methods=['POST'])
def transaction():
  if request.method == 'POST':
    # On each new POST request,
    # we extract the transaction data
    new_txion = request.get_json()
    # Then we add the transaction to our list
    this_nodes_transactions.append(new_txion)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print "New transaction"
    print "FROM: {}".format(new_txion['from'])
    print "TO: {}".format(new_txion['to'])
    print "AMOUNT: {}\n".format(new_txion['amount'])
    # Then we let the client know it worked out
    return "Transaction submission successful\n"
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def proof_of_work(last_proof):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = last_proof + 1
  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain
  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor
@node.route('/mine', methods = ['POST'])
def mine():
  if request.method == 'POST':
    new_txion = request.get_json()
    miner = int(new_txion['miner'])
    number = int(new_txion['number'])
    
    # Get the last proof of work
    user = request.args.get('user')
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
     
    if(number > last_proof and number % 9 == 0 and number % last_proof == 0):
        # Once we find a valid proof of work,
        # we know we can mine a block so 
        proof = number
        # we reward the miner by adding a transaction
        this_nodes_transactions.append(
            { "from": "network", "to": miner_address, "amount": 1 }
        )
        # Now we can gather the data needed
        # to create the new block
        new_block_data = {
            "proof-of-work": proof,
            "transactions": list(this_nodes_transactions)
        }
        new_block_index = last_block.index + 1
        new_block_timestamp = this_timestamp = date.datetime.now()
        last_block_hash = last_block.hash
        # Empty transaction list
        this_nodes_transactions[:] = []
        # Now create the
        # new block!
        mined_block = Block(
            new_block_index,
            new_block_timestamp,
            new_block_data,
            last_block_hash
        )
        blockchain.append(mined_block)
        # Let the client know we mined a block
        return json.dumps({
            "index": new_block_index,
            "timestamp": str(new_block_timestamp),
            "data": new_block_data,
            "hash": last_block_hash
        }) + "\n"


node.run()

