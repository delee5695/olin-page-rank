import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import ScalarMappable
import random


# Generate a website-like graph
def generate_website_graph(num_pages=20, connection_prob=0.3):
    G = nx.DiGraph()
    pages = [f"Page {i}" for i in range(1, num_pages + 1)]
    G.add_nodes_from(pages)
    for page in pages:
        for potential_link in pages:
            if page != potential_link and random.random() < connection_prob:
                G.add_edge(page, potential_link)
    return G


# Perform a random walk and collect visit counts at each step
def random_walk_steps(graph, start_node=None, steps=100):
    if start_node is None:
        start_node = random.choice(list(graph.nodes()))

    visit_counts = {node: 0 for node in graph.nodes()}
    visit_history = []

    current_node = start_node
    for _ in range(steps):
        visit_counts[current_node] += 1
        visit_history.append(visit_counts.copy())  # Save the current state
        neighbors = list(graph.successors(current_node))
        if neighbors:
            current_node = random.choice(neighbors)
        else:
            break  # No outgoing edges
    return visit_history


# Create the graph and random walk data
num_pages = 10
connection_prob = 0.4
steps = 50
G = generate_website_graph(num_pages, connection_prob)
start_node = random.choice(list(G.nodes()))
visit_history = random_walk_steps(G, start_node, steps)


# Normalize visit counts for animation
def normalize_visits(visit_counts):
    max_visits = max(max(v.values()) for v in visit_counts)
    return [
        {node: count / max_visits for node, count in step.items()}
        for step in visit_history
    ]


normalized_history = normalize_visits(visit_history)

# Set up the animation
fig, ax = plt.subplots(figsize=(10, 8))
pos = nx.spring_layout(G)
node_sizes = [1000] * len(G.nodes())


def update(frame):
    ax.clear()
    visit_counts = normalized_history[frame]
    node_colors = [visit_counts[node] for node in G.nodes()]
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=[v * 2000 for v in node_colors],
        node_color=node_colors,
        cmap=plt.cm.viridis,
        edge_color="gray",
        font_size=10,
        font_weight="bold",
        ax=ax,
    )
    ax.set_title(f"Random Walk Step {frame + 1}")
    sm = ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    # plt.colorbar(sm, ax=ax, label="Visit Frequency")


ani = FuncAnimation(fig, update, frames=len(normalized_history), repeat=False)
plt.show()
