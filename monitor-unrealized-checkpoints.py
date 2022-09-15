import httpx
import json
import time
import datetime
import pprint

LIGHTHOUSE_API_ENDPOINT = '<ENTER YOUR LIGHTHOUSE HTTP ENDPOINT>'
GENESIS_TIME = 1606824023

def pp(json_obj):
    pprint.pprint(json_obj, sort_dicts=False)

def get_best_checkpoints(proto_array):
    nodes = proto_array['nodes']
    indices = proto_array['indices']
    inv_indices = {v: k for k, v in indices.items()}

    best_unrealized_justified_epoch = -1
    best_unrealized_finalized_epoch = -1
    best_unrealized_justified_blocks = []
    best_unrealized_finalized_blocks = []
    
    for node in nodes:
        unrealized_justified_epoch = int(node['unrealized_justified_checkpoint']['epoch'])
        unrealized_finalized_epoch = int(node['unrealized_finalized_checkpoint']['epoch'])
        best_unrealized_justified_epoch = max(unrealized_justified_epoch, best_unrealized_justified_epoch)
        best_unrealized_finalized_epoch = max(unrealized_finalized_epoch, best_unrealized_finalized_epoch)
    
    for i in range(len(nodes)):
        block_node = nodes[i]
        block_node['block_node_index'] = i
        block_node['block_root'] = inv_indices[i]
        if int(nodes[i]['unrealized_justified_checkpoint']['epoch']) == best_unrealized_justified_epoch:
            best_unrealized_justified_blocks.append(block_node)
        if int(nodes[i]['unrealized_finalized_checkpoint']['epoch']) == best_unrealized_finalized_epoch:
            best_unrealized_finalized_blocks.append(block_node)
    
    return best_unrealized_justified_epoch, best_unrealized_justified_blocks, best_unrealized_finalized_epoch, best_unrealized_finalized_blocks

def check_fc():
    r = httpx.get(LIGHTHOUSE_API_ENDPOINT+'/lighthouse/proto_array', headers=headers)
    proto_array = r.json()['data']
    r = httpx.get(LIGHTHOUSE_API_ENDPOINT+'/eth/v1/beacon/states/head/finality_checkpoints', headers=headers)
    realized_checkpoints = r.json()['data']

    best_unrealized_justified_epoch, best_unrealized_justified_blocks, best_unrealized_finalized_epoch, best_unrealized_finalized_blocks = get_best_checkpoints(proto_array)

    min_j_block = min(best_unrealized_justified_blocks, key=lambda x: x['slot'])
    min_f_block = min(best_unrealized_finalized_blocks, key=lambda x: x['slot'])

    justified_info = {
        "Justified epoch": best_unrealized_justified_epoch,
        "Block": {
            "Root" : min_j_block['block_root'],
            "Slot" : min_j_block['slot'],
            "Slot in epoch" : int(min_j_block['slot'])%32,
            "Unrealized Justified Checkpoint": min_j_block['unrealized_justified_checkpoint'],
            "Unrealized Finalized Checkpoint": min_j_block['unrealized_finalized_checkpoint']
        }
    }

    finalized_info = {
        "Finalized epoch": best_unrealized_finalized_epoch,
        "Block": {
            "Root" : min_f_block['block_root'],
            "Slot" : min_f_block['slot'],
            "Slot in epoch" : int(min_f_block['slot'])%32,
            "Unrealized Justified Checkpoint": min_f_block['unrealized_justified_checkpoint'],
            "Unrealized Finalized Checkpoint": min_f_block['unrealized_finalized_checkpoint']
        }
    }

    return realized_checkpoints, justified_info, finalized_info

while(1):
    current_slot = int((time.time() - GENESIS_TIME) // 12)
    slot_in_epoch = current_slot%32
    current_epoch = int(current_slot//32)
    print(f"Current slot: {current_slot}, {slot_in_epoch}/32\tCurrent epoch: {current_epoch}\tTime: {datetime.datetime.now()}")
    realized_checkpoints, justified_info, finalized_info = check_fc()
    print(f"Justified - R: {realized_checkpoints['current_justified']['epoch']}, U: {justified_info['Justified epoch']}")
    print(f"Finalized - R: {realized_checkpoints['finalized']['epoch']}, U: {finalized_info['Finalized epoch']}")
    pp(realized_checkpoints)
    pp(justified_info)
    pp(finalized_info)
    for i in range(6):
        print('.', end='', flush=True)
        time.sleep(1)
    print('')