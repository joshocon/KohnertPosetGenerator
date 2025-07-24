'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

class LaTeXRenderer:
    def __init__(self):
        self.lines = ''
        self.positions = {}
        self.diagram_scale = 1
        self.node_scale = 1
        
    def set_node_positions(self, graph):
            nx_graph = nx.DiGraph()
            all_nodes = set(graph.get_vertices())
            for neighbor in graph.get_all_neighbors():
                all_nodes.update(neighbor)

            for node in all_nodes:
                nx_graph.add_node(node)
    
            for vertex, neighbors in graph.get_all_items():
                for neighbor in neighbors:
                    nx_graph.add_edge(vertex, neighbor)
    
            pos = graphviz_layout(nx_graph, prog='dot')
    
            for node, (x, y) in pos.items():
                self.set_node_position(node, x // 80, y // 30)
                self.set_diagram_tex(node)
    
    def set_node_position(self, node, x ,y):
        node.pos = (x,y)
    
    def set_diagram_tex(self, node):
        diagram = node.entry

        key = diagram.key
        x = node.pos[0]
        y = node.pos[1]

        # writing LaTeX
        string = rf'\node ({key}) at {x,y} {{\vline\tableau{{'
        for r in range(diagram.row_num, 0, -1):
            for c in range(1, diagram.col_num + 1):
                if (r, c) in diagram.cells:
                    string += r'\times'
                string += ' & ' if c != diagram.col_num else ''
            string += r'\\ '
        string += r'\hline} \hspace{3\cellsize}};'


        node.tex_string = string
        return node.tex_string

    def draw_edges(self, graph):
        draw_lines = []
        for parent in graph.get_vertices():
            for child in graph.get_neighbors(parent):
                draw_lines.append(
                    rf'\draw ({parent.entry.key}) -- ({child.entry.key});'
                )
        return '\n'.join(draw_lines)

    def generate_hasse_diagram(self, graph, root, result):

        figure_start_str = (
            fr'\begin{{figure}}[ht]\centering\begin{{tikzpicture}}[scale={self.diagram_scale}, every node/.style={{scale={self.node_scale}}}]'
            + '\n'
        )
        
        vertices = []
        seen = set()
        
        def dfs(node):
            diagram = node.entry
            frozen = frozenset(diagram.cells)
            if frozen in seen:
                return
            seen.add(frozen)

            diagram.key = diagram.generate_diagram_key(diagram.cells)
            self.set_diagram_tex(node)
            vertices.append(node.tex_string)

            for neighbor in graph.get_neighbors(node):
                dfs(neighbor)
                
        dfs(root)

        edges = self.draw_edges(graph)
        figure_end_str = (
            rf"\end{{tikzpicture}}"
            rf"\caption{{\label{{fig:poset}}{result}}}"
            rf"\end{{figure}}"
            rf"\pagebreak"
        )
        return (
            figure_start_str
            + '\n'.join(vertices)
            + '\n'
            + edges
            + '\n'
            + figure_end_str
        )
        
    def generate_initial_diagrams(self, root, result):
        figure_start_str = (
            r'\begin{figure}[ht]\centering\begin{tikzpicture}[scale=1, every node/.style={scale=0.9}]'
            + '\n'
        )
        diagram = root.entry
        
        diagram.key = diagram.generate_diagram_key(diagram.cells)
        self.set_node_position(root, 0, 0)
        self.set_diagram_tex(root)
        
        figure_end_str = (
            rf"\end{{tikzpicture}}"
            rf"\caption{{\label{{fig:poset}}{result}}}"
            rf"\end{{figure}}"
            rf"\pagebreak"
        )
        
        return figure_start_str + root.tex_string + figure_end_str