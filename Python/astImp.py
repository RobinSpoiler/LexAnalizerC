import ast
import pydot
import networkx as nx
import matplotlib.pyplot as plt

def print_ast(code):
    # Parse the code into an abstract syntax tree
    tree = ast.parse(code)
    
    # Print the AST
    print(ast.dump(tree, indent=4))

def create_ast_graph(code):
    # Parse the code into an abstract syntax tree
    tree = ast.parse(code)

    # Create a new PyDot graph
    graph_dot = pydot.Dot(graph_type='graph')

    # Create a new NetworkX graph
    graph_nx = nx.DiGraph()

    # Define a function to recursively traverse the AST and add nodes and edges to the graph
    def add_nodes_edges(node, parent=None):
        if isinstance(node, ast.AST):
            node_name = type(node).__name__
            node_id = str(id(node))
            graph_dot.add_node(pydot.Node(node_id, label=node_name))
            graph_nx.add_node(node_name)

            if parent is not None:
                graph_dot.add_edge(pydot.Edge(str(id(parent)), node_id))
                graph_nx.add_edge(parent, node_name)

            for child_name, child_node in ast.iter_fields(node):
                add_nodes_edges(child_node, node)
                if isinstance(child_node, ast.AST):
                    add_nodes_edges(child_node, node_name)
                
        elif isinstance(node, list):
            for child in node:
                add_nodes_edges(child, parent)

    # Recursively add nodes and edges to the graphs
    add_nodes_edges(tree)

    return graph_dot, graph_nx

# Example Python code
python_code = """
def example_function(x, y):
    z = x + y
    return z
"""

# Create the AST graphs
ast_graph_dot, ast_graph_nx = create_ast_graph(python_code)

# Render and display the AST graph using PyDot
ast_graph_dot.write_png("ast_graph_dot.png")

# Draw the AST graph using NetworkX and Matplotlib
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(ast_graph_nx)  # Layout for the nodes
nx.draw(ast_graph_nx, pos, with_labels=True, arrows=True)
plt.show()

# Print the AST of the example code
print_ast(python_code)
