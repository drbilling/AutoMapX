import networkx as nx
import matplotlib.pyplot as plt

def visualize_dependencies(dependencies, output_file='static/dependencies.png'):
    G = nx.DiGraph()
    for dep in dependencies:
        G.add_edge(dep[0], dep[1])
    nx.draw(G, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black')
    plt.savefig(output_file)
    plt.close()
