#!/usr/bin/env python3
import socket

HOST = "z31_server2"
PORT = 5000


class Node:
    def __init__(self, node_id, value, left_id, right_id):
        """
        :param node_id
        :param value
        :param left_id: id of the left child or -1 if none
        :param right_id: id of the right child or -1 if none
        """
        self.node_id = node_id
        self.value = value
        self.left_id = left_id
        self.right_id = right_id

    def __repr__(self):
        return f"Node(id={self.node_id}, value={self.value}, left={self.left_id}, right={self.right_id})"


def build_tree_nodes():

    nodes = []
    max_nodes = 15

    for node_id in range(max_nodes):
        left_id = 2 * node_id + 1
        right_id = 2 * node_id + 2

        if left_id >= max_nodes:
            left_id = -1
        if right_id >= max_nodes:
            right_id = -1

        value = node_id * 10

        node = Node(node_id, value, left_id, right_id)
        nodes.append(node)

    return nodes


def send_tree(nodes):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))
    print("Connected, sending nodes")

    for node in nodes:
        line = f"{node.node_id} {node.value} {node.left_id} {node.right_id}\n"
        data = line.encode("utf-8")

        print(f"sending: {line.strip()}")
        s.sendall(data)

    print("All nodes sent, closing socket")
    s.close()


def main():
    nodes = build_tree_nodes()
    print("generated nodes:")
    for n in nodes:
        print(n)

    send_tree(nodes)


if __name__ == "__main__":
    main()
