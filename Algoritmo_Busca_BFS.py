#=====================================================================================================#
# Universidade Federal do Pará
# Faculdade de Computação
# Prof: Roberto Samarone
# Aluno: Mário Diego 
#=====================================================================================================#


#============================= Algoritmo de Busca em Largura - BFS ===================================#
# Algoritmo de Busca em Largura - BFS segundo (CORMEM et al., 2009)
# Primeira Versão Clássica


#-ATIVAR OS PACOTES
from collections import deque, defaultdict

class Grafo:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = defaultdict(list)

    def adicionar_aresta(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)  # Se for grafo não direcionado

    def bfs(self, inicio):
        cor = {v: 'branco' for v in self.adj}
        distancia = {v: float('inf') for v in self.adj}
        antecessor = {v: None for v in self.adj}

        cor[inicio] = 'cinza'
        distancia[inicio] = 0

        fila = deque()
        fila.append(inicio)

        while fila:
            u = fila.popleft()
            for v in self.adj[u]:
                if cor[v] == 'branco':
                    cor[v] = 'cinza'
                    distancia[v] = distancia[u] + 1
                    antecessor[v] = u
                    fila.append(v)
            cor[u] = 'preto'

        return distancia, antecessor

    def reconstruir_caminho(self, antecessor, inicio, destino):
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = antecessor[atual]
        caminho.reverse()
        if caminho[0] == inicio:
            return caminho
        else:
            return []

    def encontrar_tamanho_e_caminho(self, inicio, destino):
        if inicio not in self.adj or destino not in self.adj:
            return f"Erro: vértice(s) inválido(s)."

        distancia, antecessor = self.bfs(inicio)
        dist = distancia[destino]

        if dist == float('inf'):
            return f"Não existe caminho entre {inicio} e {destino}."
        else:
            caminho = self.reconstruir_caminho(antecessor, inicio, destino)
            return f"Tamanho do Menor Caminho: {dist} arestas\nCaminho: {' -> '.join(map(str, caminho))}"



#-Criando o grafo
grafo = Grafo(vertices=8)


#-Adicionando as arestas conforme o exemplo do Cormen
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(1, 6)
grafo.adicionar_aresta(1, 7)
grafo.adicionar_aresta(1, 8)
grafo.adicionar_aresta(2, 8)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 4)
grafo.adicionar_aresta(3, 6)
grafo.adicionar_aresta(3, 7)
grafo.adicionar_aresta(4, 5)
grafo.adicionar_aresta(4, 8)
grafo.adicionar_aresta(5, 5)
grafo.adicionar_aresta(5, 6)
grafo.adicionar_aresta(6, 7)
grafo.adicionar_aresta(7, 8)

# Entrada do usuário
inicio = int(input("DIGITAR VÉRTICE INICIAL: "))
destino = int(input("DIGITAR VÉRTICE DE DESTINO: "))

# Saída
resultado = grafo.encontrar_tamanho_e_caminho(inicio, destino)
print(resultado)
#=====================================================================================================#



#=====================================================================================================#
# Segunda Versão - Progresso do Algoritmo (Visual) 

#-ATIVAR OS PACOTES
from collections import deque, defaultdict
import networkx as nx
import matplotlib.pyplot as plt


class Grafo:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = defaultdict(list)

    def adicionar_aresta(self, u, v):
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)  # Grafo não direcionado

    def bfs(self, inicio):
        cor = {v: 'branco' for v in self.adj}
        distancia = {v: float('inf') for v in self.adj}
        antecessor = {v: None for v in self.adj}

        cor[inicio] = 'cinza'
        distancia[inicio] = 0

        fila = deque()
        fila.append(inicio)

        while fila:
            u = fila.popleft()
            for v in sorted(self.adj[u]):  # ordem crescente
                if cor[v] == 'branco':
                    cor[v] = 'cinza'
                    distancia[v] = distancia[u] + 1
                    antecessor[v] = u
                    fila.append(v)
            cor[u] = 'preto'

        return distancia, antecessor

    def reconstruir_caminho(self, antecessor, inicio, destino):
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = antecessor[atual]
        caminho.reverse()
        if caminho[0] == inicio:
            return caminho
        else:
            return []

    def encontrar_tamanho_e_caminho(self, inicio, destino):
        if inicio not in self.adj or destino not in self.adj:
            return f"Erro: vértice(s) inválido(s)."

        distancia, antecessor = self.bfs(inicio)
        dist = distancia[destino]

        if dist == float('inf'):
            return f"Não Existe Caminho Entre {inicio} e {destino}."
        else:
            caminho = self.reconstruir_caminho(antecessor, inicio, destino)
            return f"Tamanho do Menor Caminho: {dist} arestas\nCaminho: {' -> '.join(map(str, caminho))}", caminho

    def desenhar_grafo(self, caminho_destacado=None):
        G = nx.Graph()
        for u in self.adj:
            for v in self.adj[u]:
                G.add_edge(u, v)

        # Ordenar os nós 
        ordenados = sorted(G.nodes())
        
        # Layout em forma de círculo com nós ordenados
        pos = nx.shell_layout(G, nlist=[ordenados])  # centralizado e ordenado

        # Desenho do grafo
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
                node_size = 800, font_size = 12, edge_color='gray')

        if caminho_destacado:
            edges_caminho = [(caminho_destacado[i], caminho_destacado[i+1]) for i in range(len(caminho_destacado)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges_caminho, edge_color='red', width=3)

        plt.title("Visualização do Grafo com Caminho Destacado")
        plt.axis('off')
        plt.show()


#-Definir vértices
vertices = ['1', '2', '3', '4', '5', '6', '7', '8']

# Criando o grafo
grafo = Grafo(vertices)

# Adicionando arestas
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(1, 6)
grafo.adicionar_aresta(1, 7)
grafo.adicionar_aresta(1, 8)
grafo.adicionar_aresta(2, 8)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 4)
grafo.adicionar_aresta(3, 6)
grafo.adicionar_aresta(3, 7)
grafo.adicionar_aresta(4, 5)
grafo.adicionar_aresta(4, 8)
grafo.adicionar_aresta(5, 5)
grafo.adicionar_aresta(5, 6)
grafo.adicionar_aresta(6, 7)
grafo.adicionar_aresta(7, 8)


# Entrada do usuário
inicio = int(input("DIGITAR VÉRTICE INICIAL: "))
destino = int(input("DIGITAR VÉRTICE DE DESTINO: "))

# Resultado
resultado = grafo.encontrar_tamanho_e_caminho(inicio, destino)
if isinstance(resultado, tuple):
    texto, caminho = resultado
    print(texto)
    grafo.desenhar_grafo(caminho_destacado=caminho)
else:
    print(resultado)
    grafo.desenhar_grafo()
#=====================================================================================================#









