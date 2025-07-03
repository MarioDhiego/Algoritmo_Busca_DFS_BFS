#=====================================================================================================#
# Universidade Federal do Pará
# Faculdade de Computação
# Prof: Roberto Samarone
# Aluno: Mário Diego 
#=====================================================================================================#


#============================= Algoritmo de Busca em Produndidade - DFS ==============================#
# Algoritmo de Busca - DFS segundo (CORMEM et al., 2009)
# Primeira Versão Clássica


#-Ativar Pacotes
from collections import defaultdict

# Classe Grafo com Lista de Adjacência
class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = defaultdict(list)
        self.tempo = 0

    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)

    def dfs(self):
        # Inicialização
        self.cor = {v: 'BRANCO' for v in self.vertices}
        self.pai = {v: None for v in self.vertices}
        self.d = {v: 0 for v in self.vertices}
        self.f = {v: 0 for v in self.vertices}
        self.tempo = 0

        print("Início da DFS:")
        for u in self.vertices:
            if self.cor[u] == 'BRANCO':
                print(f"\nIniciando DFS-VISIT em {u}")
                self.dfs_visit(u)

    def dfs_visit(self, u):
        self.cor[u] = 'CINZA'
        self.tempo += 1
        self.d[u] = self.tempo
        print(f"Visitando {u}: cor={self.cor[u]}, d={self.d[u]}")

        for v in self.grafo[u]:
            print(f"  Explorando aresta ({u}, {v})")
            if self.cor[v] == 'BRANCO':
                print(f"    {v} está BRANCO. Antecessor de {v} = {u}")
                self.pai[v] = u
                self.dfs_visit(v)
            else:
                print(f"    {v} já foi visitado: cor={self.cor[v]}")

        self.cor[u] = 'PRETO'
        self.tempo += 1
        self.f[u] = self.tempo
        print(f"Finalizando {u}: cor={self.cor[u]}, f={self.f[u]}")

#-Mostrar Resultados Finais 
    def imprimir_resultado(self):
        print("\nResultado Final:")
        print("Vértice | Descoberta | Finalização | Pai | Cor Final")
        for v in self.vertices:
            print(f"{v:^7} | {self.d[v]:^10} | {self.f[v]:^12} | {str(self.pai[v]):^5} | {self.cor[v]}")

#-Definindo os vértices
vertices = ['r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#-Criando o grafo
g = Grafo(vertices)

#-Adicionando as arestas conforme o exemplo do Cormen
g.adicionar_aresta('r', 's')
g.adicionar_aresta('r', 't')
g.adicionar_aresta('r', 'w')
g.adicionar_aresta('s', 't')
g.adicionar_aresta('s', 'x')
g.adicionar_aresta('t', 'u')
g.adicionar_aresta('t', 'y')
g.adicionar_aresta('u', 'v')
g.adicionar_aresta('u', 'x')
g.adicionar_aresta('v', 'y')
g.adicionar_aresta('y', 'x')
g.adicionar_aresta('x', 'v')
g.adicionar_aresta('w', 'y')
g.adicionar_aresta('w', 'z')
g.adicionar_aresta('z', 'z')  # laço

#-Executando DFS
g.dfs()

#-Exibindo resultados
g.imprimir_resultado()
#=====================================================================================================#



#=====================================================================================================#
# Segunda Versão - Progresso do Algoritmo (Visual) 

# Ativar Pacotes
import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import clear_output
import time


class GrafoVisualQuadros:
    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = {v: [] for v in vertices}
        self.tempo = 0
        self.G = nx.DiGraph()
        self.G.add_nodes_from(vertices)
        self.pos = nx.spring_layout(self.G, seed=42)

        self.historico = []  # Armazena (titulo, cor de cada nó)

    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)
        self.G.add_edge(u, v)

    def dfs(self):
        self.cor = {v: 'BRANCO' for v in self.vertices}
        self.pai = {v: None for v in self.vertices}
        self.d = {}
        self.f = {}
        self.tempo = 0

        for u in self.vertices:
            if self.cor[u] == 'BRANCO':
                self.dfs_visit(u)

    def dfs_visit(self, u):
        self.tempo += 1
        self.d[u] = self.tempo
        self.cor[u] = 'CINZA'
        self.salvar_estado(f"Visitando {u}: CINZA")

        for v in self.grafo[u]:
            if self.cor[v] == 'BRANCO':
                self.pai[v] = u
                self.dfs_visit(v)

        self.cor[u] = 'PRETO'
        self.tempo += 1
        self.f[u] = self.tempo
        self.salvar_estado(f"Finalizando {u}: PRETO")

    def salvar_estado(self, titulo):
        cores_mapeadas = {'BRANCO': 'white', 'CINZA': 'gray', 'PRETO': 'black'}
        estado = [cores_mapeadas[self.cor[v]] for v in self.G.nodes]
        self.historico.append((titulo, list(estado)))  # Cópia do estado

    def mostrar_quadros(self):
        n_quadros = len(self.historico)
        cols = min(n_quadros, 4)
        rows = (n_quadros + cols - 1) // cols

        plt.figure(figsize=(5 * cols, 4 * rows))

        for i, (titulo, estado_cores) in enumerate(self.historico):
            plt.subplot(rows, cols, i + 1)
            nx.draw(self.G, pos=self.pos, with_labels=True,
                    node_color=estado_cores, node_size=1200,
                    edge_color='black', font_color='black')
            plt.title(titulo)
        plt.tight_layout()
        plt.show()

    def imprimir_resultado(self):
        print("\nResultado Final:")
        print("Vértice | Descoberta | Finalização | Pai | Cor Final")
        for v in self.vertices:
            print(f"{v:^7} | {self.d[v]:^10} | {self.f[v]:^12} | {str(self.pai[v]):^5} | {self.cor[v]}")

#-Definir vértices
vertices = ['r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#-Criar o grafo com quadros
gq = GrafoVisualQuadros(vertices)

#-Adicionar arestas (exemplo do livro Cormen)
gq.adicionar_aresta('r', 's')
gq.adicionar_aresta('r', 't')
gq.adicionar_aresta('r', 'w')
gq.adicionar_aresta('s', 't')
gq.adicionar_aresta('s', 'x')
gq.adicionar_aresta('t', 'u')
gq.adicionar_aresta('t', 'y')
gq.adicionar_aresta('u', 'v')
gq.adicionar_aresta('u', 'x')
gq.adicionar_aresta('v', 'y')
gq.adicionar_aresta('y', 'x')
gq.adicionar_aresta('x', 'v')
gq.adicionar_aresta('w', 'y')
gq.adicionar_aresta('w', 'z')
gq.adicionar_aresta('z', 'z')  # laço

#-Executar DFS
gq.dfs()

#-Mostrar quadros lado a lado
gq.mostrar_quadros()

#-Imprimir resultado final
gq.imprimir_resultado()
#=====================================================================================================#

















