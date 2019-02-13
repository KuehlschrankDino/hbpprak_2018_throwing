import os
import json_tricks as json
import argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dir',
                        help='Path to json files',
                        required = True,
                        type = str,
                        default="")
    args = parser.parse_args()

    return args

def read_distance(output_path):
    dirFiles = os.listdir(output_path)
    fileList = sorted([os.path.join(output_path, f) for f in os.listdir(output_path) if f.endswith('.json')])
    distances = []
    for i, json_file_path in enumerate(fileList):
    
        
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            distances.append(data[0]["distance"])

    return np.array(distances)



if __name__ == '__main__':
    args = parse_args()
    np.save("all_distances.npy", read_distance(args.dir))