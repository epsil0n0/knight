from collections import deque
from flask import Flask, request
import json


# queue node used in BFS
class Node:
    # (x, y) represents chess board coordinates
    # dist represent its minimum distance from the source
    def __init__(self, x, y, dist=0, node=None):
        if not isinstance(x, int):
            raise TypeError(f'got {type(x)} type, expected int.')
        if not isinstance(y, int):
            raise TypeError(f'got {type(y)} type, expected int.')
        if not isinstance(dist, int):
            raise TypeError(f'got {type(dist)} type, expected int.')
        if node is not None and not isinstance(node, Node):
            raise TypeError(f'got {type(node)} type, expected int.')
        self.x = x
        self.y = y
        self.dist = dist
        self.parent = node

    def _str_(self):
        return f'< x:{self.x}, y:{self.y} >'

    def __repr__(self):
        return f'< x:{self.x}, y:{self.y} >'


# Below lists details all 8 possible movements for a knight
row = (2, 2, -2, -2, 1, 1, -1, -1)
col = (-1, 1, 1, -1, 2, -2, 2, -2)


# Check if (x, y) is valid chess board coordinates
# Note that a knight cannot go out of the chessboard
def valid(x, y, n):
    return not (x < 0 or y < 0 or x >= n or y >= n)

path = []

def print_path(node):
    if node is None:
        return
    print_path(node.parent)
    path.append([node.x, node.y])
    print(node)



# Find minimum number of steps taken by the knight
# from source to reach destination using BFS
def BFS(source, destination, n):
    # set to check if matrix cell is visited before or not
    visited = set()

    # create a queue and enqueue first node
    queue = deque()
    queue.append(source)

    # run till queue is not empty
    while queue:

        # pop front node from queue and process it
        node = queue.popleft()

        x = node.x
        y = node.y
        dist = node.dist

        # if destination is reached, return distance
        if x == destination.x and y == destination.y:
            return node

        # Skip if location is visited before
        if node not in visited:
            # mark current node as visited
            visited.add(node)

            # check for all 8 possible movements for a knight
            # and enqueue each valid movement into the queue
            for i in range(8):
                # Get the valid position of Knight from current position on
                # chessboard and enqueue it with +1 distance
                x1 = x + row[i]
                y1 = y + col[i]

                if valid(x1, y1, n):
                    queue.append(Node(x1, y1, dist + 1, node))

    # return None if path is not possible
    return None


# if __name__ == '__main__':
#     N = 8
#     src = Node(0, 7)  # source coordinates
#     dest = Node(7, 0)  # destination coordinates
#     answer = BFS(src, dest)
#     if answer is not None:
#         print("Minimum number of steps required is ", answer.dist)
#         print("The complete path is: ")
#         print_path(answer)
#     else:
#         print("Path is not possible.")


# Creating a Web App
app = Flask(__name__)


@app.route('/', methods=['POST'])
def solve():
    raw_data = request.get_json()
    N = raw_data['n']
    src = Node(raw_data['start_x'], raw_data['start_y'])  # source coordinates
    dest = Node(raw_data['end_x'], raw_data['end_y'])  # destination coordinates
    answer = BFS(src, dest, N)
    if answer is not None:
        print_path(answer)
        response = {"Minimum number of steps required is": answer.dist,
                    "The complete path is:": path}
    else:
        response = {
            "message": "Path is not possible."
        }
    return json.dumps(response), 201


#if __name__ == '__main__':
#    print("starting...")
#    app.run(host='0.0.0.0', port=5000, debug=True)
