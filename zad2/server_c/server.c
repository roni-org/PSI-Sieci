#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 5000
#define MAX_NODES 15
#define BUF_SIZE 256

struct Node {
    int id;
    int value;
    struct Node *left;
    struct Node *right;
};

struct Node nodes[MAX_NODES];
int left_ids[MAX_NODES];
int right_ids[MAX_NODES];

void initStorage() {
    for (int i = 0; i < MAX_NODES; i++) {
        nodes[i].id = i;
        nodes[i].value = 0;
        nodes[i].left = NULL;
        nodes[i].right = NULL;
        left_ids[i] = -1;
        right_ids[i] = -1;
    }
}

void linkTree() {
    for (int i = 0; i < MAX_NODES; i++) {
        if (left_ids[i] != -1) {
            nodes[i].left = &nodes[left_ids[i]];
        } else {
            nodes[i].left = NULL;
        }

        if (right_ids[i] != -1) {
            nodes[i].right = &nodes[right_ids[i]];
        } else {
            nodes[i].right = NULL;
        }
    }
}


void printPreorder(struct Node *node) {
    if (node == NULL) return;
    printf("Node id=%d value=%d\n", node->id, node->value);
    printPreorder(node->left);
    printPreorder(node->right);
}



void printPreorderToFile(struct Node *node, FILE *f) {
    if (node == NULL || f == NULL) return;

    fprintf(f, "Node id=%d value=%d\n", node->id, node->value);
    printPreorderToFile(node->left, f);
    printPreorderToFile(node->right, f);
}


int main() {
    int server_fd, client_fd;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);
    char buffer[BUF_SIZE];

    initStorage();


    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }


    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }


    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);


    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }


    if (listen(server_fd, 1) < 0) {
        perror("listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d...\n", PORT);


    client_fd = accept(server_fd, (struct sockaddr *)&address, &addrlen);
    if (client_fd < 0) {
        perror("accept failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Client connected.\n");

     char line[BUF_SIZE];
    int pos = 0;

    printf("Receiving data...\n");

    while (1) {
        char c;
        int bytes = recv(client_fd, &c, 1, 0);

        if (bytes == 0) {

            printf("Client disconnected.\n");
            break;
        }
        if (bytes < 0) {
            perror("recv failed");
            break;
        }

            if (c == '\n') {

            line[pos] = '\0';

            printf("Received line: %s\n", line);

            int id, value, left_id, right_id;


            int parsed = sscanf(line, "%d %d %d %d", &id, &value, &left_id, &right_id);
            if (parsed == 4) {
                if (id >= 0 && id < MAX_NODES) {
                    nodes[id].value = value;
                    left_ids[id] = left_id;
                    right_ids[id] = right_id;

                    printf("Stored: id=%d value=%d left_id=%d right_id=%d\n",
                           id, value, left_id, right_id);
                } else {
                    fprintf(stderr, "Warning: invalid id=%d in line: %s\n", id, line);
                }
            } else {
                fprintf(stderr, "Warning: cannot parse line: %s\n", line);
            }

            pos = 0;
        }
	 else {
            if (pos < BUF_SIZE - 1) {
                line[pos++] = c;
            }
        }
    }

    printf("Finished receiving.\n");
    linkTree();

    printf("Tree (preorder):\n");
    printPreorder(&nodes[0]);

   FILE *f = fopen("tree_preorder.txt", "w");
    if (f == NULL) {
        perror("fopen failed");
    } else {
        fprintf(f, "Tree (preorder):\n");
        printPreorderToFile(&nodes[0], f);
        fclose(f);
        printf("Tree written to tree_preorder.txt\n");
    }
    printf("Closing connection.\n");
    close(client_fd);
    close(server_fd);

    return 0;
}
