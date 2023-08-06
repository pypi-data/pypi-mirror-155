import h5py
import matplotlib.pyplot as plt


class Node:
    def __init__(self,
                 name: str):
        self.to = []
        self.name = name

    def add_node(self, to):
        self.to.append(to)

    @property
    def n_out(self):
        return len(self.to)


class Edges:
    def __init__(self,
                 from_node: Node,
                 to_node: Node):
        self.from_node = from_node
        self.to_node = to_node


class Graph:
    def __init__(self, list_nodes: list, list_edges: list):
        self.list_nodes = self.register_nodes(list_nodes)
        self.list_edges = self.register_edges(list_edges)

    @staticmethod
    def register_nodes(list_nodes: list):
        nodes = dict()
        for node_name in set(list_nodes):
            node = Node(name=node_name)
            nodes[node_name] = node
        return nodes

    def register_edges(self, list_edges: list):
        edges = list()
        for edge in set(list_edges):
            node_from = self.list_nodes[edge[0]]
            node_to = self.list_nodes[edge[1]]
            node_from.add_node(to=node_to)
            it_edge = Edges(from_node=node_from, to_node=node_to)
            edges.append(it_edge)
        return edges

    def to_hdf5(self, file_name: str):
        with h5py.File(file_name, 'w') as f:
            f.create_dataset('node_list',
                             data=[item for item, _ in self.list_nodes.items()])
            f.create_dataset('edge_list',
                             data=[(item.from_node.name, item.to_node.name) for item in self.list_edges])

    @staticmethod
    def read_hdf5(file_name: str):
        with h5py.File(file_name, 'r') as f:
            node_list = list(f.get('node_list'))
            edge_list = [tuple(item) for item in list(f.get('edge_list'))]
            graph = Graph(list_nodes=node_list, list_edges=edge_list)
        return graph

    def plot_histogram_degree_out(self, image_name: str = 'hist.png', n_bins: int = 20):
        plt.hist(self.vertex_out_degree, bins=n_bins)
        plt.xlabel('number vertices out')
        plt.ylabel('counts')
        plt.grid()
        plt.title('Vertex Out Degree')
        plt.savefig(image_name)

    @property
    def vertex_out_degree(self):
        return [item.n_out for _, item in self.list_nodes.items()]

    @property
    def n_nodes(self):
        return len(self.list_nodes)

    @property
    def n_edges(self):
        return len(self.list_edges)
