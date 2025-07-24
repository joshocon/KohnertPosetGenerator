'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

from src import Diagram, Graph, DiagramEngine, LaTeXRenderer, KohnertPoset, SoutheastDiagramGenerator, ProgessBar
import subprocess
import ast

def main():
    sdg = SoutheastDiagramGenerator()
    #sdg.generate(4,4) #generates all nxn southeast diagrams and writes it to diagrams.txt
    
    def ask_bool(prompt):
        return input(prompt + " (y/n): ").strip().lower() == 'y'

    compile_latex = ask_bool("Compile LaTeX?")
    draw_full_poset = False
    if compile_latex:
        draw_full_poset = ask_bool("Draw full poset?")
    
    test_boundedness = ask_bool("Test boundedness?")
    test_rankedness = ask_bool("Test rankedness?")
    test_monomial_multiplicity_free = ask_bool("Test monomial multiplicity-freeness?")


    diagrams = []
    with open('diagrams.txt', 'r') as file:
        data = file.readlines()
    
    for line in data:
        raw_cells = line.strip().split(' ')
        cells = [ast.literal_eval(cell) for cell in raw_cells ]
        diagrams.append(sdg.normalize_cells(cells))
        
    latex_start = r'''
    \documentclass{article}
    \usepackage{graphicx, geometry, amsmath, amsfonts, tikz, youngtab, cite}
    \geometry{left=2cm, right=2cm}
    \savebox2{%
    \begin{picture}(12,12)
    \put(0,0){\line(1,0){12}}
    \put(0,0){\line(0,1){12}}
    \put(12,0){\line(0,1){12}}
    \put(0,12){\line(1,0){12}}
    \end{picture}}
    \newcommand\cover{\mathrel{\ooalign{$\prec$\cr
    \hidewidth\hbox{$\cdot\mkern0.5mu$}\cr}}}
    \newlength\cellsize
    \setlength\cellsize{12pt} 
    \newcommand\cellify[1]{\def\thearg{#1}\def\nothing{}%
    \ifx\thearg\nothing\vrule width0pt height\cellsize depth0pt%
    \else\hbox to 0pt{\usebox2\hss}\fi%
    \vbox to 12\unitlength{\vss\hbox to 12\unitlength{\hss$#1$\hss}\vss}}
    \newcommand\tableau[1]{\vtop{\let\\=\cr
    \setlength\baselineskip{-12000pt}
    \setlength\lineskiplimit{12000pt}
    \setlength\lineskip{0pt}
    \halign{&\cellify{##}\cr#1\crcr}}}
    \savebox4{% CIRCLE
    \begin{picture}(12,12)
    \put(6,6){\circle{12}}
    \end{picture}}
    \newcommand{\cir}[1]{\def\thearg{#1}\def\nothing{}%
    \ifx\thearg\nothing\vrule width0pt height\cellsize depth0pt%
    \else\hbox to 0pt{\usebox4\hss}\fi%
    \vbox to 12\unitlength{\vss\hbox to 12\unitlength{\hss$#1$\hss}\vss}}
    \newcommand\nocellify[1]{\def\thearg{#1}\def\nothing{}%
    \ifx\thearg\nothing\vrule width0pt height\cellsize depth0pt%
    \else\hbox to 0pt{\hss}\fi%
    \vbox to 12\unitlength{\vss\hbox to 12\unitlength{\hss$#1$\hss}\vss}}
    \newcommand\notableau[1]{\vtop{\let\\=\cr
    \setlength\baselineskip{-12000pt}
    \setlength\lineskiplimit{12000pt}
    \setlength\lineskip{0pt}
    \halign{&\nocellify{##}\cr#1\crcr}}}
    \title{Code Generation of Posets}
    \begin{document}
    \maketitle '''
    latex_hasse_diagrams = []
    latex_initial_diagrams = []
    kohnert_results = []
    latex_end = r'\end{document}'
    
    progress = ProgessBar(len(diagrams))

    for index, cells in enumerate(diagrams, 1):
        graph = Graph()
        engine = DiagramEngine()
        renderer = LaTeXRenderer()
        
        row_num, col_num = engine.get_dimension(cells)
        diagram = Diagram(list(cells), row_num, col_num) 
        graph.add_vertex(diagram) 
        D_0 = graph.get_root_node()
        
        if diagram.cells == []:
            print('Error')
        
        elif engine.check_south_east(diagram.cells) == False:
           print(f'\nNot Southeast: {diagram.cells}')
        
        else:
            engine.kohnert_move(graph, diagram)
            
            kohnert_poset = KohnertPoset(graph)

            if test_boundedness:
                result = kohnert_poset.boundedness_result()
                test = diagram.test_bounded_conjecture()
                
                kohnert_results.append(f'{result}' + f' ||| Conjecture Result: {test}')
                
            if test_rankedness:
                result = kohnert_poset.rankedness_result()
                test = diagram.test_ranked_conjecture()
                
                kohnert_results.append(f'{result}' + f' ||| Conjecture Result: {test}')
                
            if test_monomial_multiplicity_free:
                result = kohnert_poset.monomial_multiplicity_free_result()
                test = diagram.test_mmf_conjecture()
                
                kohnert_results.append(f'{result}' + f' ||| Conjecture Result: {test}')
            
            if compile_latex:
            
                if draw_full_poset: 
                    renderer.set_node_positions(graph)
                    latex_hasse_diagrams.append(renderer.generate_hasse_diagram(graph, D_0, result))
                    
                if not draw_full_poset:
                    latex_initial_diagrams.append(renderer.generate_initial_diagrams(D_0, result +' | '+ test))
                    
            progress.print_progress(index)
    print() 
    
    with open('output.txt', 'w') as f:
                f.write('\n'.join(kohnert_results))
                    
    failed_to_meet = 0
    should_not_meet = 0
    filter_criteria1 = 'True ||| Conjecture Result: M'
    filter_criteria2 = 'False ||| Conjecture Result: F'
    output_list = []

    with open('output.txt', 'r') as f:
        for line in f:
            start = line.find('[') + 1
            end = line.find(']')
            
            if filter_criteria2 in line or filter_criteria1 in line:
                if filter_criteria1 in line:
                    should_not_meet += 1
                if filter_criteria2 in line: 
                    failed_to_meet += 1
                diagram = line[start:end]
                diagram = diagram.replace('),', ')')
                diagram = diagram.replace(', ', ',')
                output_list.append(diagram)

    print(f'{failed_to_meet} failed to meet')
    print(f'{should_not_meet} should not have met')        
    output_list.sort(key=len)
    
    string = '\n'.join(output_list)
    
    with open('formatted.txt', 'w') as f:
        f.write(string)
    
    if compile_latex:
    
        with open('main.tex', 'w') as f:
                    f.write(latex_start + '\n'.join(latex_hasse_diagrams) + '\n'.join(latex_initial_diagrams) + latex_end)
                        
        with open('latex_errors.log', 'w') as error_log:
                    subprocess.run(['pdflatex','-interaction=nonstopmode', 'main.tex'], stdout=subprocess.DEVNULL, stderr=error_log)

if __name__ == '__main__':
    main()