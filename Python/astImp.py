import ast

def print_ast(code):
    # Parse the code into an abstract syntax tree
    tree = ast.parse(code)
    
    # Print the AST
    print(ast.dump(tree, indent=4))
import ast
import pydot

def create_ast_graph(code):
    # Parse the code into an abstract syntax tree
    tree = ast.parse(code)

    # Create a new PyDot graph
    graph = pydot.Dot(graph_type='graph')

    # Define a function to recursively traverse the AST and add nodes and edges to the graph
    def add_nodes_edges(node, parent=None):
        if isinstance(node, ast.AST):
            node_name = type(node).__name__
            node_id = str(id(node))
            graph.add_node(pydot.Node(node_id, label=node_name))

            if parent is not None:
                graph.add_edge(pydot.Edge(str(id(parent)), node_id))

            for child_name, child_node in ast.iter_fields(node):
                add_nodes_edges(child_node, node)
        elif isinstance(node, list):
            for child in node:
                add_nodes_edges(child, parent)

    # Recursively add nodes and edges to the graph
    add_nodes_edges(tree)

    return graph

# Example Python code
# python_code = """
# def example_function(x, y):
#     z = x + y
#     return z
# """

# Create the AST graph
# ast_graph = create_ast_graph(python_code)

# Render and display the AST graph
# ast_graph.write_png("ast_graph.png")

# Example Python code
# python_code = """
# def example_function(x, y):
#     z = x + y
#     return z
# """

# # Print the AST of the example code
# print_ast(python_code)
