import networkx as nx  # FOUND THIS LIBRARY THAT HAD THE IMPLEMENTATION OF MINIMUM CUT :D
import time 


def main():
    with open('./december_25/input.txt') as f:
        lines = f.readlines()

    graph = nx.Graph()
    for line in lines:
        line = line.strip()
        first_node = line.split(': ')[0]
        connections = line.split(': ')[1].split(' ')
        for connection in connections:
            node1 = first_node
            node2 = connection
            graph.add_edge(node1, node2, capacity=1)


    solution = 0
    init_t = time.time()
    for node in graph.nodes():
        source_node = node
        for node in graph.nodes():
            sink_node = node
            if source_node == sink_node:
                continue
            # compute the minimum cut
            cut_value, partition = nx.minimum_cut(graph, source_node, sink_node)
            if cut_value == 3:
                solution = len(partition[0]) * len(partition[1])
                break
    print(f'Part 1 took {time.time() - init_t} seconds')
    print(f'Part 1: {solution}')

    # Part 2	
    
if __name__ == '__main__':
    main()