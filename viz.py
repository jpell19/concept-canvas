
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import numpy as np

G = nx.Graph()

# Add nodes to the graph
G.add_nodes_from(range(10))

# Set node attributes for color and frequency
for node in G.nodes():
    G.nodes[node]['color'] = np.random.randint(0, 10)
    G.nodes[node]['frequency'] = np.random.uniform(0.1, 0.5)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a list of node colors and frequencies
node_colors = [G.nodes[node]['color'] for node in G.nodes()]
node_freqs = [G.nodes[node]['frequency'] for node in G.nodes()]

# Create a position dictionary for the nodes
pos = nx.spring_layout(G, dim=3)

xs = [pt[0] for pt in pos.values()]
ys = [pt[1] for pt in pos.values()]
zs = [pt[2] for pt in pos.values()]

# Draw the nodes with colors and frequencies
nodes = ax.scatter(xs, ys, zs, c=node_colors, cmap=plt.cm.Set3, s=100, alpha=1.0)


# Set up the animation function to update the node positions
def update(num):
    pos = nx.spring_layout(G, dim=3, k=0.2, iterations=num)
    nodes._offsets3d = ([pt[0] for pt in pos.values()], [pt[1] for pt in pos.values()], [pt[2] for pt in pos.values()])
    return nodes,

# Animate the node positions
ani = FuncAnimation(fig, update, frames=range(100), interval=50)

# Set the axis limits and labels
ax.set_xlim3d([-1, 1])
ax.set_ylim3d([-1, 1])
ax.set_zlim3d([-1, 1])
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Show the plot
plt.show()
