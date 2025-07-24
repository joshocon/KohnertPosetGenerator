from .diagram import Diagram

class DiagramEngine:
    
    def get_dimension(self, cells):
        row_num = 0
        col_num = 0
        for cell in cells:
            if row_num < cell[0]:
                row_num = cell[0]
            if col_num < cell[1]:
                col_num = cell[1]
        return [row_num, col_num]

    def check_south_east(self, cells):
        cells_set = set(cells)
        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                if (
                    min(cells[i][0], cells[j][0]),
                    max(cells[i][1], cells[j][1]),
                ) not in cells_set:
                    return False
        return True
    
    def check_north_east(self, cells):
        cells_set = set(cells)
        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                if (
                    max(cells[i][0], cells[j][0]),
                    max(cells[i][1], cells[j][1]),
                ) not in cells_set:
                    return False
        return True

    def find_move_cells(self, diagram):
        cells = set(diagram.cells)
        max_cells = {}

        for (r, c) in cells:
            if r not in max_cells or c > max_cells[r][1]:
                max_cells[r] = (r, c)

        elementary_moves = []
        jump_moves = []

        for cell in max_cells.values():
            row, col = cell
            for r_below in range(row - 1, 0, -1): 
                if (r_below, col) not in cells:
                    is_elementary = (row == r_below + 1)
                    move = [cell, (r_below, col), is_elementary]
                    if is_elementary:
                        elementary_moves.append(move)
                    else:
                        jump_moves.append(move)
                    break  
        return elementary_moves, jump_moves

    
    def kohnert_move(self, graph, diagram, cache=None, jump_visited=None):
        if cache is None:
            cache = {}
        if jump_visited is None:
            jump_visited = set()

        def build_elementary(diagram):
            key = frozenset(diagram.cells)
            graph.add_vertex(diagram)
            cache[key] = diagram

            elementary_moves, _ = self.find_move_cells(diagram)
            for old_cell, new_cell, is_elem in elementary_moves:
                new_cells = list(diagram.cells)
                if old_cell not in new_cells:
                    continue
                new_cells.remove(old_cell)
                new_cells.append(new_cell)
                new_diagram = Diagram(new_cells, diagram.row_num, diagram.col_num)
                new_key = frozenset(new_diagram.cells)
                graph.add_vertex(new_diagram)
                graph.add_edge(diagram, new_diagram)
                if new_key not in cache:
                    build_elementary(new_diagram)

        def explore_jumps(diagram):
            key = frozenset(diagram.cells)
            if key in jump_visited:
                return
            jump_visited.add(key)

            _, jump_moves = self.find_move_cells(diagram)
            for old_cell, new_cell, is_elem in jump_moves:
                new_cells = list(diagram.cells)
                if old_cell not in new_cells:
                    continue
                new_cells.remove(old_cell)
                new_cells.append(new_cell)
                new_diagram = Diagram(new_cells, diagram.row_num, diagram.col_num)
                new_key = frozenset(new_diagram.cells)

                # Only add if diagram not already found via elementary moves
                if new_key not in cache:
                    graph.add_vertex(new_diagram)
                    graph.add_edge(diagram, new_diagram)
                    cache[new_key] = new_diagram
                    build_elementary(new_diagram) 
                    explore_jumps(new_diagram)   
                           
        build_elementary(diagram)
        for d in list(cache.values()):
            explore_jumps(d)
        return diagram



