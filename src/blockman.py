from block import *


def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  new_block_data = {
    "proof-of-work": 18874368,
    "transactions": ""
  }
  return Block(0, date.datetime.now(), new_block_data, "0")

def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.hash
  
  return Block(this_index, this_timestamp, this_data, this_hash)
