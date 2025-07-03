#=====================================================================================================#
# Universidade Federal do Pará
# Faculdade de Computação
# Prof: Roberto Samarone
# Aluno: Mário Diego 
#=====================================================================================================#


#============================= Algoritmo de Busca em Profundidade com ciclos- DFS ====================#
# Algoritmo de Busca em Profundidade - DFS segundo (CORMEM et al., 2009)
# Primeira Versão Clássica


#-ATIVAR OS PACOTES
from collections import defaultdict

class Grafo:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = defaultdict(list)
        self.ciclo_encontrado = []
        self.visitando = True

    def adicionar_aresta(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)  # Grafo não direcionado

    def dfs_com_ciclo(self):
        cor = {v: 'branco' for v in self.adj}
        antecessor = {v: None for v in self.adj}
        for v in self.adj:
            if cor[v] == 'branco' and self.visitando:
                self.dfs_visit(v, cor, antecessor)

        if self.ciclo_encontrado:
            print("Ciclo encontrado:", ' -> '.join(map(str, self.ciclo_encontrado)))
        else:
            print("Nenhum ciclo encontrado.")

    def dfs_visit(self, u, cor, antecessor):
        cor[u] = 'cinza'
        for v in self.adj[u]:
            if not self.visitando:
                return
            if cor[v] == 'branco':
                antecessor[v] = u
                self.dfs_visit(v, cor, antecessor)
            elif cor[v] == 'cinza' and v != antecessor[u]:
                # Ciclo detectado!
                self.ciclo_encontrado = self.reconstruir_ciclo(antecessor, u, v)
                self.visitando = False
                return
        cor[u] = 'preto'

    def reconstruir_ciclo(self, antecessor, u, v):
        ciclo = [v, u]
        while u != v and antecessor[u] is not None:
            u = antecessor[u]
            ciclo.append(u)
            if u == v:
                break
        ciclo.reverse()
        return ciclo


# ---------------------- EXEMPLO DE USO ---------------------------#
grafo = Grafo(vertices = 10)

# Criando um grafo com ciclo
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 9)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 4)
grafo.adicionar_aresta(4, 9)
grafo.adicionar_aresta(8, 6)
grafo.adicionar_aresta(9, 10)
grafo.adicionar_aresta(10, 1)

# Adicionando arestas fora do ciclo (opcional)
grafo.adicionar_aresta(4, 5)
grafo.adicionar_aresta(5, 6)
grafo.adicionar_aresta(6, 7)
grafo.adicionar_aresta(7, 8)
grafo.adicionar_aresta(2, 9)
grafo.adicionar_aresta(5, 9)

# Rodar DFS com detecção de ciclo
grafo.dfs_com_ciclo()
#=====================================================================================================#



#=====================================================================================================#
# Segunda Versão - Progresso do Algoritmo (Visual) 

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict
from IPython.display import HTML, display


class Grafo:
    def __init__(self):
        self.adj = defaultdict(list)
        self.ciclo_encontrado = []
        self.visitando = True
        self.frames = []
        self.G = nx.Graph()

    def adicionar_aresta(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.G.add_edge(u, v)

    def dfs_com_ciclo(self):
        cor = {v: 'branco' for v in self.adj}
        antecessor = {v: None for v in self.adj}
        for v in self.adj:
            if cor[v] == 'branco' and self.visitando:
                self.dfs_visit(v, cor, antecessor)

        if not self.frames:
            self.registrar_frame(cor)

    def dfs_visit(self, u, cor, antecessor):
        cor[u] = 'cinza'
        self.registrar_frame(cor)

        for v in self.adj[u]:
            if not self.visitando:
                return
            if cor[v] == 'branco':
                antecessor[v] = u
                self.dfs_visit(v, cor, antecessor)
            elif cor[v] == 'cinza' and v != antecessor[u]:
                self.ciclo_encontrado = self.reconstruir_ciclo(antecessor, u, v)
                self.visitando = False
                self.registrar_frame(cor, ciclo=self.ciclo_encontrado)
                return

        cor[u] = 'preto'
        self.registrar_frame(cor)

    def reconstruir_ciclo(self, antecessor, u, v):
        ciclo = [v, u]
        while u != v and antecessor[u] is not None:
            u = antecessor[u]
            ciclo.append(u)
            if u == v:
                break
        ciclo.reverse()
        return ciclo

    def registrar_frame(self, cor, ciclo=None):
        frame = {
            'cor': cor.copy(),
            'ciclo': ciclo.copy() if ciclo else None
        }
        self.frames.append(frame)

    def animar(self):
        pos = nx.spring_layout(self.G, seed=42)
        fig, ax = plt.subplots(figsize=(8, 6))

        def desenhar(i):
            ax.clear()
            frame = self.frames[i]
            cor_atual = frame['cor']
            ciclo = frame.get('ciclo', [])

            cor_nos = []
            for n in self.G.nodes():
                estado = cor_atual.get(n, 'branco')
                if estado == 'branco':
                    cor_nos.append('white')
                elif estado == 'cinza':
                    cor_nos.append('gray')
                else:
                    cor_nos.append('black')

            nx.draw(self.G, pos, with_labels=True, ax=ax,
                    node_color=cor_nos, edge_color='lightgray', node_size=800)

            if ciclo and len(ciclo) > 1:
                arestas_ciclo = [(ciclo[i], ciclo[i+1]) for i in range(len(ciclo)-1)]
                arestas_ciclo.append((ciclo[-1], ciclo[0]))  # fecha o ciclo
                nx.draw_networkx_edges(self.G, pos, edgelist=arestas_ciclo, edge_color='red', width=3)

            ax.set_title(f"Passo {i+1}/{len(self.frames)}", fontsize=14)
            ax.axis('off')

        self.ani = animation.FuncAnimation(fig, desenhar, frames=len(self.frames),
                                           interval=1000, repeat=False)
        plt.close()
        return HTML(self.ani.to_jshtml())



grafo = Grafo()

# Criando um grafo com ciclo
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 9)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 4)
grafo.adicionar_aresta(4, 9)
grafo.adicionar_aresta(8, 6)
grafo.adicionar_aresta(9, 10)
grafo.adicionar_aresta(10, 1)

# Arestas extras fora do ciclo
grafo.adicionar_aresta(4, 5)
grafo.adicionar_aresta(5, 6)
grafo.adicionar_aresta(6, 7)
grafo.adicionar_aresta(7, 8)
grafo.adicionar_aresta(2, 9)
grafo.adicionar_aresta(5, 9)

# Rodar DFS com detecção de ciclo
grafo.dfs_com_ciclo()

# Mostrar animação
display(grafo.animar())
#=====================================================================================================#























