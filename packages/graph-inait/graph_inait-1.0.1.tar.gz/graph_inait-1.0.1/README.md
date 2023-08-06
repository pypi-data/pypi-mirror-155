# Inait's Graph Representation
Graph class with the following characteristics:
- Be constructed from a list of vertices and a list of pairs of vertices indicating the edges.
- Print the number of vertices and edges.
- Serialize and deserialize to/from HDF5.
- Plot a histogram of vertex out-degrees (the number of edges coming out of each vertex)

# How to install it
Package is available in PyPi. To install it just  use pip
```
pip install inait_graph
```

# Quick Tutorial
Please find an online-reproducible notebook in this [link](https://colab.research.google.com/drive/1g9baRG590EORI_OoCd_KiK-9s79xqtJ_?usp=sharing).
### 1. Instance a Graph object
To instantiate a Graph object it is required a list of vertices and a list of pair of vertices as in the code shown below.
```
nodes = [1, 2, 3, 4, 5]
edges = [(1, 2),
         (2, 3),
         (3, 4),
         (4, 5),
         (5, 1)]
graph = Graph(list_nodes=nodes, list_edges=edges)
```

### 2. Get graph information
```
# Get number of nodes
print(graph.n_nodes)

# Get number of edges
print(graph.n_edges)

# Serialize graph to HDF5
graph.to_hdf5(file_name='ex.h5')

# Build graph from HDF5 file
graph.read_hdf5(file_name='ex.h5')

# Save PNG file with histogram degree out.
graph.plot_histogram_degree_out()
```

# Miscellaneous
TBD:
- Detect cycles
- Breadth first search.
 