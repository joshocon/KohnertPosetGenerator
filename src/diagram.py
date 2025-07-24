'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

import hashlib

class Diagram:
    def __init__(self, cells, row_num, col_num):
        self.cells = cells
        self.zero_index = [(r-1,c-1) for (r,c) in self.cells]
        self.row_num = row_num
        self.col_num = col_num
        self.key = None
        self.row_weight = None
        self.column_weight = None
        self.monomial = None
        self.set_column_weight()
        
    # gives diagram a unique key
    def generate_diagram_key(self, cells):
        sorted_cells = sorted(cells)
        cell_str = str(sorted_cells)
        return hashlib.md5(cell_str.encode()).hexdigest()

    def set_row_weight(self):
        weight = {}
        if self.cells != []:
            for r,c in self.cells:
                r = int(r)  # Ensure r is int
                weight[r] = weight.get(r, 0) + 1

            max_row = max(weight.keys(), default=0)
            row_weight = [weight.get(r, 0) for r in range(1, max_row + 1)]
        self.row_weight = row_weight
    
    def set_column_weight(self):
        weight = {}
        if self.cells != []:
            for r, c in self.cells:
                c = int(c)  # Ensure c is int
                weight[c] = weight.get(c, 0) + 1

            max_col = max(weight.keys(), default=0)
            column_weight = [weight.get(c, 0) for c in range(1, max_col + 1)]
        self.column_weight = column_weight
    
    def get_monomial(self):
        monomial = ''
        for i in range(len(self.row_weight)):
            if self.row_weight[i] != 0:
                if self.row_weight[i] == 1:
                    monomial += f'x_{i+1}'
                else:
                    monomial += f'x_{i+1}^{self.row_weight[i]}'
        return monomial

    def get_row_number(self):
        return self.row_num

    def get_col_number(self):
        return self.col_num
    
    def test_bounded_conjecture(self):
        def condition_a_and_b():
            #three cells such that r1 = r2 < r3 and c1 < c2 = c3
            satisfied = []
            n = len(self.zero_index)
            for i in range(n):
                r1,c1 = self.zero_index[i]
                for j in range(n):
                    r2,c2 = self.zero_index[j]
                    for k in range(n):
                        r3,c3 = self.zero_index[k]
                        #make sure all cells are unique
                        if len({(r1,c1), (r2,c2), (r3,c3)}) != 3:
                            continue
                        if r1 == r2 < r3 and c1 < c2 == c3:
                            satisfied.append(tuple(sorted([(r1, c1), (r2, c2), (r3, c3)])))
            return (list(t) for t in set(satisfied))

        def condition_c(trio):
            r1,c1 = trio[0]
            r2,c2 = trio[1]
            return True
            return all(self.column_weight[c] < self.column_weight[c2] for c in range(c1, c2))
    
        def condition_d(trio):
            #there is an empty space beneath r1 for all  c1 <= c <= c2
            r1,c1 = trio[0]
            r2,c2 = trio[1]
            
            if r1 == 0:
                return False
            
            def count_below(r,c):
                for i in range(1, r1 + 1):
                    if (r - i, c) not in self.zero_index:
                       return True
                return False
            
            return all(count_below(r1,c) for c in range(c1, self.col_num))

        
        def condition_e(trio):
            # For r1 and c > c2 where , if (r1, c) in the diagram, there must be no cells below it
            r1, c1 = trio[0]
            r2, c2 = trio[1]
            
            def count_below(col):
                for row in range(r2 - 1, -1, -1): 
                    if (row, col) not in self.zero_index:
                        return True
                return False
            
            for r,c in self.zero_index:
                if r == r1 and c > c2:
                    if count_below(c):
                        return False
            return True
            
    
        def condition_f(trio):
            #for r1 < r the cell (r,c1) not in the diagram
            r1,c1 = trio[0]
            return all((r,c1) not in self.zero_index for r in range(r1 + 1,self.row_num))
        
        def condition_g(trio):
            # If there is a cell at (r, c1) for r > r1, then row_weight[r] > 1
            return True
            r1, c1 = trio[0]
            for r in range(r1 + 1, self.row_num):
                if (r, c1) in self.zero_index:
                    if self.row_weight[r] <= 1:
                        return False
            return True

        
        def condition_h(trio):
            #for c > c2 cwt(D)c < r2
            r2,c2 = trio[1]
            return True
            return all(self.column_weight[c] <= r2 for c in range(c2 + 1, self.col_num))
            
        good_trios = condition_a_and_b()
        
        possible_failures = {'fails C', 'fails D', 'fails E', 'fails F', 'fails G', 'fails H'}#, 'fails I', 'fails J'}

        for trio in good_trios:
            c_res = condition_c(trio)
            d_res = condition_d(trio)
            e_res = condition_e(trio)
            f_res = condition_f(trio)
            g_res = condition_g(trio)
            h_res = condition_h(trio)
            #print(f'{trio}: {c_res}, {d_res}, {e_res}, {f_res}, {g_res}, {h_res}')
            #i_res = condition_i(trio)
            #j_res = condition_j(trio)

            if c_res and e_res and f_res and d_res:# and e_res and f_res and g_res and h_res: # and i_res and j_res:
                return f'Meets with {trio}'
            if c_res:
                possible_failures.discard('fails C')
            if d_res:
                possible_failures.discard('fails D')
            if e_res:
                possible_failures.discard('fails E')
            if f_res:
                possible_failures.discard('fails F')
            if g_res:
                possible_failures.discard('fails G')
            if h_res:
                possible_failures.discard('fails H')
            # if i_res:
            #     possible_failures.discard('fails I')
            # if j_res:
            #     possible_failures.discard('fails J')
                
        return f'Fails: {sorted(possible_failures)}'
    
    def test_ranked_conjecture(self):
        
        def condition_a_and_b():
            #three cells such that  r2 <= r1 < r3 and c1 < c2 and c3 = c2 or c3 = c1
            satisfied = []
            n = len(self.zero_index)
            for i in range(n):
                r1,c1 = self.zero_index[i]
                for j in range(n):
                    r2,c2 = self.zero_index[j]
                    for k in range(n):
                        r3,c3 = self.zero_index[k]
                        #make sure all cells are unique
                        if len({(r1,c1), (r2,c2), (r3,c3)}) != 3:
                            continue
                        if ((r2 <= r1 < r3) or (r3 < r2 <= r1)) and ((c1 < c2) and (c3 == c2 or c3 == c1)):
                            satisfied.append(tuple([(r1, c1), (r2, c2), (r3, c3)]))
            return satisfied
        
        def condition_c(triple):
            r1, c1 = triple[0]
            r2, c2 = triple[1]
            r3, c3 = triple[2]
            
            rmin = min(r1,r2,r3)
            
            def count_below(col):
                for row in range(rmin - 1, -1, -1): 
                    if (row, col) not in self.zero_index:
                        return True
                return False
                
            def count_two_below(col):
                count = 0
                for row in range(rmin - 1, -1, -1): 
                    if (row, col) not in self.zero_index:
                        count += 1
                        if count >= 2:
                            return True
                return False
            
            if rmin == 0 :
                return False
            if c3 == c2:
                return all(count_below(c) for c in range(c1, c2 + 1))
            if c3 == c1:
                return count_two_below(c1) and all(count_below(c) for c in range(c1 + 1, c2 + 1))
                

        
        def condition_d(triple):
            return True

        good_triples = condition_a_and_b()
        
        possible_failures = {'fails C', 'fails D'}
        for triple in good_triples:
            c_res = condition_c(triple)
            d_res = condition_d(triple)
            
            if c_res:
                possible_failures.discard('fails C')
            if d_res:
                possible_failures.discard('fails D')
            
            if c_res and d_res:
                return f'Meets with {triple}'
            
        
        return f'Fails: {sorted(possible_failures)}'
    
    def test_mmf_conjecture(self):
        #if there exist cells (r1,c1) and (r2,c2) such that r1 >= r2 and c1 < c2 with at least two open spaces beneath each 
    
        def condition_a_and_b():
            #three cells such that  r2 <= r1 < r3 and c1 < c2 and c3 = c2 or c3 = c1
            satisfied = []
            n = len(self.zero_index)
            for i in range(n):
                r1,c1 = self.zero_index[i]
                for j in range(n):
                    r2,c2 = self.zero_index[j]
                    for k in range(n):
                        r3,c3 = self.zero_index[k]
                        #make sure all cells are unique
                        if len({(r1,c1), (r2,c2), (r3,c3)}) != 3:
                            continue
                        if r2 <= r1 < r3 and c1 < c2 and (c3 == c2 or c3 == c1):
                            satisfied.append(tuple([(r1, c1), (r2, c2), (r3, c3)]))
            return satisfied
        
        def condition_c(triple):
            #there are at least two empty spaces beneath every row for c1 <= c <= c2
            r1, c1 = triple[0]
            r2, c2 = triple[1]

            if r1 == 0 or r2 == 0:
                return False

            def count_below(col):
                count = 0
                for row in range(r2 - 1, -1, -1): 
                    if (row, col) not in self.zero_index:
                        count += 1
                    if count >= 2:
                        return True
                return False

            return all(count_below(c) for c in range(c1, self.col_num))


        def condition_d(triple):
           r2,c2 = triple[1]
           return True
           
                
        def condition_e(triple):
            
            return True
 
        def condition_f(triple):
            #there is at least one empty cell in each column below r2 for c > c2
            return True
            r2,c2 = triple[1]
            def count_below(col):
                for row in range(r2 - 1, -1, -1): 
                    if (row, col) not in self.zero_index:
                        return True
                return False
            return all(count_below(c) for c in range(c2 + 1, self.col_num))
        
        def condition_g(triple):
            return True

        
        good_triple = condition_a_and_b()
        
        possible_failures = {'fails C', 'fails D', 'fails E', 'fails F', 'fails G'}
        for triple in good_triple:
            
            c_res = condition_c(triple)
            d_res = condition_d(triple)
            e_res = condition_e(triple)
            f_res = condition_f(triple)
            g_res = condition_g(triple)

            #print(f'{triple}: {c_res}, {d_res}, {e_res}, {f_res}')
            if c_res:
                possible_failures.discard('fails C')
            if d_res:
                possible_failures.discard('fails D')
            if e_res:
                possible_failures.discard('fails E')
            if f_res:
                possible_failures.discard('fails F')
            if g_res:
                possible_failures.discard('fails G')
                
            if c_res and d_res and e_res and f_res and g_res:
                return f'Meets with {triple}'
        
        return f'Fails: {sorted(possible_failures)}'
            

                    
    def __eq__(self, other):
        return isinstance(other, Diagram) and set(self.cells) == set(other.cells)

    def __hash__(self):
        return hash(frozenset(self.cells))

    def __repr__(self):
        return f'{self.cells}'