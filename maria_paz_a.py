import networkx as nx # Importa NetworkX para grafos.
import matplotlib.pyplot as plt # Importa Matplotlib para visualização.
import heapq # Importa heapq para fila de prioridade (Dijkstra, A*).

# === 1. CRIAÇÃO E VISUALIZAÇÃO DO GRAFO ===

# Inicializa um grafo direcionado (MultiDiGraph permite múltiplas arestas).
grafo_dir = nx.MultiDiGraph()

# Adiciona arestas com pesos ao grafo.
grafo_dir.add_edge('x', 'y', weight=1)
grafo_dir.add_edge('y', 'x', weight=1)
grafo_dir.add_edge('x', 'z', weight=2)
grafo_dir.add_edge('x', 'w', weight=3)
grafo_dir.add_edge('z', 'y', weight=1)
grafo_dir.add_edge('w', 'z', weight=1)
grafo_dir.add_edge('z', 'w', weight=2)
grafo_dir.add_edge('y', 'z', weight=1)

# Define coordenadas para visualização dos nós.
coords_nos = {
    'x': (0, 1),
    'y': (1, 1),
    'z': (1, 0),
    'w': (0, 0)
}

# Desenha nós e seus rótulos.
nx.draw_networkx_nodes(grafo_dir, coords_nos, node_size=800, node_color='lightblue')
nx.draw_networkx_labels(grafo_dir, coords_nos, font_size=14, font_color='black')

# Desenha arestas, ajustando o estilo para arestas múltiplas.
for origem, destino, chave in grafo_dir.edges(keys=True):
    estilo = 'arc3, rad=0.1' if chave == 0 else 'arc3, rad=-0.1'
    nx.draw_networkx_edges(grafo_dir, coords_nos, edgelist=[(origem, destino)], connectionstyle=estilo)

# Adiciona rótulos de peso às arestas.
pesos_rotulo = {(u, v): d['weight'] for u, v, d in grafo_dir.edges(data=True)}
for (inicio, fim), valor in pesos_rotulo.items():
    x1, y1 = coords_nos[inicio]
    x2, y2 = coords_nos[fim]
    x_txt = x1 * 0.9 + x2 * 0.1
    y_txt = y1 * 0.9 + y2 * 0.1
    plt.text(x_txt, y_txt, str(valor),
             bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'),
             horizontalalignment='center')

# Configura e exibe o plot do grafo.
plt.axis('off')
plt.title("Grafo Direcionado com Pesos")
plt.show()

# === 2. RAÍZES E FOLHAS ===

# Encontra nós com grau de entrada zero (raízes) e grau de saída zero (folhas).
def encontrar_raizes_folhas(g):
    origem_zeros = [n for n, grau in g.in_degree() if grau == 0]
    destino_zeros = [n for n, grau in g.out_degree() if grau == 0]
    return origem_zeros, destino_zeros

# Chama a função e imprime os resultados.
nos_iniciais, nos_finais = encontrar_raizes_folhas(grafo_dir)
print("Nós de entrada:", nos_iniciais)
print("Nós de saída:", nos_finais)

# === 3. GRAUS DE ENTRADA E SAÍDA ===

# Calcula os graus de saída para todos os nós.
graus_saida = {n: grafo_dir.out_degree(n) for n in grafo_dir.nodes()}
# Calcula os graus de entrada para todos os nós.
graus_entrada = {n: grafo_dir.in_degree(n) for n in grafo_dir.nodes()}

# Imprime os graus.
print("Grau de saída:", graus_saida)
print("Grau de entrada:", graus_entrada)

# === 4. CAMINHOS E CICLOS ===

print("\nCaminhos simples de 'x' para 'y':")
# Imprime todos os caminhos simples de 'x' para 'y'.
for p in nx.all_simple_paths(grafo_dir, source='x', target='y'):
    print(" -> ".join(p))

# Verifica se o grafo é acíclico.
eh_acíclico = nx.is_directed_acyclic_graph(grafo_dir)
print("É acíclico?", "Sim" if eh_acíclico else "Não")

# Tenta encontrar e imprimir um ciclo, se houver.
try:
    ciclo = nx.find_cycle(grafo_dir)
    print("Ciclo encontrado:", ciclo)
except nx.NetworkXNoCycle:
    print("Sem ciclos detectados.")

# === 5. MOCHILA FRACIONÁRIA ===

# Implementa o algoritmo guloso para a mochila fracionária.
def mochila_fracionada(valores, pesos, capacidade):
    # Cria itens com (valor, peso, razão valor/peso, índice).
    itens = [(v, p, v/p, i) for i, (v, p) in enumerate(zip(valores, pesos))]
    # Ordena itens por razão valor/peso (decrescente).
    itens.sort(key=lambda x: x[2], reverse=True)

    total = 0
    resto = capacidade
    fracoes = [0] * len(valores)

    # Adiciona itens à mochila.
    for v, p, _, i in itens:
        if p <= resto: # Item cabe totalmente.
            fracoes[i] = 1
            total += v
            resto -= p
        else: # Item não cabe totalmente.
            fracoes[i] = resto / p
            total += v * fracoes[i]
            break
    return total, fracoes

# Dados e chamada da função.
lucros = [60, 100, 120]
pesagens = [10, 20, 30]
cap_limite = 50
lucro_total, uso_itens = mochila_fracionada(lucros, pesagens, cap_limite)

# Imprime resultados.
print("\nLucro total:", lucro_total)
print("Frações por item:", uso_itens)

# Plota as frações utilizadas dos itens.
plt.figure(figsize=(8, 5))
plt.bar(range(len(lucros)), uso_itens, tick_label=[f"Item {i}" for i in range(len(lucros))], color='orchid')
plt.title(f'Mochila Fracionada - Total: {lucro_total:.2f}')
plt.ylim(0, 1.1)
for i, f in enumerate(uso_itens):
    plt.text(i, f + 0.03, f"{f*100:.1f}%", ha='center')
plt.tight_layout()
plt.show()

# === 6. SELEÇÃO DE ATIVIDADES ===

# Implementa a seleção de atividades de forma iterativa (guloso).
def agendar_atividades(inicio_lst, fim_lst):
    # Ordena eventos pelo tempo de término.
    eventos = sorted(zip(inicio_lst, fim_lst), key=lambda x: x[1])
    agenda, fim_ant = [], -1
    # Agenda atividades não conflitantes.
    for ini, fim in eventos:
        if ini >= fim_ant:
            agenda.append((ini, fim))
            fim_ant = fim
    return agenda

# Implementa a seleção de atividades de forma recursiva (guloso).
def agendar_recursivo(ini_lst, fim_lst, fim_ant=-1, i=0):
    if i >= len(ini_lst): # Caso base.
        return []
    if ini_lst[i] >= fim_ant: # Atividade pode ser agendada.
        return [(ini_lst[i], fim_lst[i])] + agendar_recursivo(ini_lst, fim_lst, fim_lst[i], i+1)
    else: # Atividade conflitua.
        return agendar_recursivo(ini_lst, fim_lst, fim_ant, i+1)

# Dados e chamada das funções.
iniciais = [1, 3, 0, 5, 8, 5]
finais = [2, 4, 6, 7, 9, 9]
agenda_iterativa = agendar_atividades(iniciais, finais)

ordem_agenda = sorted(zip(iniciais, finais), key=lambda x: x[1])
in_ord, fin_ord = zip(*ordem_agenda)
agenda_recursiva = agendar_recursivo(in_ord, fin_ord)

# Imprime resultados.
print("\nAgenda (iterativa):", agenda_iterativa)
print("Agenda (recursiva):", agenda_recursiva)

# Plota o agendamento de atividades.
plt.figure(figsize=(10, 4))
for ini, fim in zip(iniciais, finais):
    plt.barh(1, fim - ini, left=ini, height=0.4, color='lightgray')
for ini, fim in agenda_iterativa:
    plt.barh(1, fim - ini, left=ini, height=0.4, color='green')
plt.title("Agendamento de Atividades (Guloso)")
plt.yticks([1], ["Agenda"])
plt.xlabel("Tempo")
plt.tight_layout()
plt.show()

# === 7. TROCO MÍNIMO ===

# Implementa o problema do troco mínimo usando programação dinâmica.
def troco_minimo(moedas_disp, valor):
    dp = [float('inf')] * (valor + 1) # dp[i] = min moedas para valor i.
    dp[0] = 0

    # Preenche a tabela dp.
    for i in range(1, valor + 1):
        for moeda in moedas_disp:
            if i - moeda >= 0:
                dp[i] = min(dp[i], dp[i - moeda] + 1)
    return dp

# Dados e chamada da função.
moedas_entrada = [1, 3, 4]
valor_troco = 10
min_moedas = troco_minimo(moedas_entrada, valor_troco)

# Plota a quantidade mínima de moedas para cada valor.
plt.figure(figsize=(8, 5))
plt.bar(range(valor_troco + 1), min_moedas, color='gold')
plt.title("Troco Mínimo (Coin Change)")
plt.xlabel("Valor")
plt.ylabel("Qtd. Mínima de Moedas")
plt.tight_layout()
plt.show()

# === 8. DIJKSTRA ===

# Implementa o algoritmo de Dijkstra para o caminho mais curto de uma fonte.
def menor_caminho_dijkstra(g, inicio):
    dist = {n: float('inf') for n in g.nodes}
    dist[inicio] = 0
    fila = [(0, inicio)] # Fila de prioridade (distância, nó).
    anterior = {} # Para reconstrução do caminho.

    while fila:
        atual_dist, atual = heapq.heappop(fila)

        if atual_dist > dist[atual]: # Já encontrou caminho mais curto.
            continue

        for viz in g[atual]:
            peso = g[atual][viz][0]['weight']
            nova_dist = atual_dist + peso
            if nova_dist < dist[viz]: # Caminho mais curto encontrado para vizinho.
                dist[viz] = nova_dist
                anterior[viz] = atual
                heapq.heappush(fila, (nova_dist, viz))
    return dist, anterior

# Chama Dijkstra e reconstrói o caminho de 'x' para 'y'.
distancias_x, caminhos_x = menor_caminho_dijkstra(grafo_dir, 'x')
trajeto = []
no = 'y'
while no != 'x':
    trajeto.append((caminhos_x[no], no))
    no = caminhos_x[no]
trajeto.reverse()

# Plota o grafo com o caminho de Dijkstra destacado.
plt.figure()
nx.draw(grafo_dir, coords_nos, with_labels=True, node_color='lightgreen', node_size=800)
nx.draw_networkx_edges(grafo_dir, coords_nos, edgelist=trajeto, edge_color='green', width=2)
plt.title("Caminho Mais Curto com Dijkstra (x → y)")
plt.tight_layout()
plt.show()

# === 9. A* ===

# Função heurística para A* (distância euclidiana).
def distancia_heuristica(a, b):
    x1, y1 = coords_nos[a]
    x2, y2 = coords_nos[b]
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# Implementa o algoritmo A* para encontrar o caminho mais curto.
def caminho_a_estrela(g, ini, alvo):
    fila = [(0, ini)] # Fila de prioridade (prioridade, nó).
    custos = {ini: 0} # Custo do caminho do início até o nó.
    pais = {} # Para reconstrução do caminho.

    while fila:
        _, atual = heapq.heappop(fila)

        if atual == alvo: # Caminho encontrado.
            break

        for viz in g[atual]:
            peso = g[atual][viz][0]['weight']
            novo_custo = custos[atual] + peso
            if viz not in custos or novo_custo < custos[viz]: # Caminho mais curto encontrado para vizinho.
                custos[viz] = novo_custo
                prioridade = novo_custo + distancia_heuristica(viz, alvo)
                heapq.heappush(fila, (prioridade, viz))
                pais[viz] = atual
    return pais

# Chama A* e reconstrói o caminho de 'x' para 'y'.
pais_estrela = caminho_a_estrela(grafo_dir, 'x', 'y')
trajeto_astar = []
n = 'y'
while n != 'x':
    trajeto_astar.append((pais_estrela[n], n))
    n = pais_estrela[n]
trajeto_astar.reverse()

# Plota o grafo com o caminho de A* destacado.
plt.figure()
nx.draw(grafo_dir, coords_nos, with_labels=True, node_color='lightcoral', node_size=800)
nx.draw_networkx_edges(grafo_dir, coords_nos, edgelist=trajeto_astar, edge_color='red', width=2)
plt.title("Caminho A* de x para y")
plt.tight_layout()
plt.show()
