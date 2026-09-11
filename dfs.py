# Source - https://stackoverflow.com/q/77539424
# Posted by just coding, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-07, License - CC BY-SA 4.0

import matplotlib.pyplot as plt


graph = {
  'S' : ['A','B', 'C'],
  'A' : ['D'],
  'B' : ['E'],
  'C' : ['F', 'J'],
  'D' : ['G'],
  'E' : ['I', 'J'],
  'F' : ['S'],
  'J' : [],
  'G' : ['H'],
  'I' : [],
  'J' : [],
  'H' : ['D']
}

visited = [] # List for visited nodes.
queue = []     #Initialize a queue

def bfs(visited, graph, node): #function for BFS
  order = []
  visited.append(node)
  queue.append(node)

  while queue:          # Creating loop to visit each node
    m = queue.pop(0) 
    print(m, end = " ")
    order.append(m)

    for neighbour in graph[m]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

  return order


def draw_graph(graph, order):
  positions = {
    'S': (0, 2), 'A': (-2, 1), 'B': (0, 1), 'C': (2, 1),
    'D': (-2, 0), 'E': (0, 0), 'F': (2, 0), 'J': (3, -1),
    'G': (-2, -1), 'I': (0, -1), 'H': (-2, -2)
  }
  visit_numbers = {node: number for number, node in enumerate(order, 1)}

  figure, axis = plt.subplots(figsize=(10, 7))
  for source, neighbours in graph.items():
    for target in neighbours:
      start_x, start_y = positions[source]
      end_x, end_y = positions[target]
      axis.annotate(
        '', xy=(end_x, end_y), xytext=(start_x, start_y),
        arrowprops={'arrowstyle': '->', 'color': '#94a3b8', 'lw': 1.5}
      )

  for node, (x_position, y_position) in positions.items():
    color = '#22c55e' if node in visit_numbers else '#cbd5e1'
    axis.scatter(x_position, y_position, s=1500, color=color,
                 edgecolors='#0f172a', linewidths=1.5, zorder=3)
    label = f'{node}\n#{visit_numbers[node]}' if node in visit_numbers else node
    axis.text(x_position, y_position, label, ha='center', va='center',
              fontsize=11, fontweight='bold', zorder=4)

  axis.set_title('Breadth-First Search Traversal', fontsize=16, fontweight='bold')
  axis.text(0, -2.5, ' -> '.join(order), ha='center', fontsize=11)
  axis.set_xlim(-3, 4)
  axis.set_ylim(-3, 3)
  axis.axis('off')
  figure.tight_layout()
  output_file = 'bfs_visualization.png'
  figure.savefig(output_file, dpi=160, bbox_inches='tight')
  print(f"\nVisual graph saved to {output_file}")

# Driver Code
print("Following is the Breadth-First Search")
traversal_order = bfs(visited, graph, 'S')    # function calling
draw_graph(graph, traversal_order)
