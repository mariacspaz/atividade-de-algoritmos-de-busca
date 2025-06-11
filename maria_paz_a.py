import networkx as nx
import matplotlib.pyplot as plt
import heapq

# === 1. CONSTRUÇÃO E VISUALIZAÇÃO DO GRAFO ===

rede_direcionada = nx.MultiDiGraph()

rede_direcionada.add_edge('x', 'y', weight=1)
rede_direcionada.add_edge('y', 'x', weight=1)
rede_direcionada.add_edge('x', 'z', weight=2)
rede_direcionada.add_edge('x', 'w', weight=3)
rede_direcionada.add_edge('z', 'y', weight=1)
rede_direcionada.add_edge('w', 'z', weight=1)
rede_direcionada.add_edge('z', 'w', weight=2)
rede_direcionada.add_edge('y', 'z', weight=1)

posicoes_nos = {
    'x': (0, 1),
    'y': (1, 1),
    'z': (1, 0),
    'w': (0, 0)
}

nx.draw_networkx_nodes(rede_direcionada, posicoes_nos, node_size=800, node_color='lightblue')
nx.draw_networkx_labels(rede_direcionada, posicoes_nos, font_size=14, font_color='black')

for origem, destino, chave in rede_direcionada.edges(keys=True):
    estilo_conexao = 'arc3, rad=0.1' if chave == 0 else 'arc3, rad=-0.1'
    nx.draw_networkx_edges(rede_direcionada, posicoes_nos, edgelist=[(origem, destino)], connectionstyle=estilo_conexao)

rotulos_pesos = {(u, v): d['weight'] for u, v, d in rede_direcionada.edges(data=True)}
for (inicio, fim), valor in rotulos_pesos.items():
    x1, y1 = posicoes_nos[inicio]
    x2, y2 = posicoes_nos[fim]
    x_texto = x1 * 0.9 + x2 * 0.1
    y_texto = y1 * 0.9 + y2 * 0.1
    plt.text(x_texto, y_texto, str(valor),
             bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'),
             horizontalalignment='center')

plt.axis('off')
plt.title("Visualização do Grafo Direcionado com Pesos")
plt.show()

# === 2. IDENTIFICAÇÃO DE NÓS RAIZ E FOLHA ===

def identificar_nos_raiz_folha(grafo):
    nos_raiz = [no for no, grau in grafo.in_degree() if grau == 0]
    nos_folha = [no for no, grau in grafo.out_degree() if grau == 0]
    return nos_raiz, nos_folha

raizes, folhas = identificar_nos_raiz_folha(rede_direcionada)
print("Nódulos raiz:", raizes)
print("Nódulos folha:", folhas)

# === 3. RAMIFICAÇÕES DE ENTRADA E SAÍDA ===

ramificacao_saida = {no: rede_direcionada.out_degree(no) for no in rede_direcionada.nodes()}
ramificacao_entrada = {no: rede_direcionada.in_degree(no) for no in rede_direcionada.nodes()}

print("Ramificações de saída:", ramificacao_saida)
print("Ramificações de entrada:", ramificacao_entrada)

# === 4. CAMINHOS E CICLOS ===

print("\nCaminhos simples de 'x' para 'y':")
for caminho in nx.all_simple_paths(rede_direcionada, source='x', target='y'):
    print(" -> ".join(caminho))

grafo_e_acíclico = nx.is_directed_acyclic_graph(rede_direcionada)
print("O grafo é acíclico?", "Sim" if grafo_e_acíclico else "Não")

try:
    ciclo_encontrado = nx.find_cycle(rede_direcionada)
    print("Ciclo detectado:", ciclo_encontrado)
except nx.NetworkXNoCycle:
    print("Nenhum ciclo encontrado.")

# === 5. MOCHILA FRACIONÁRIA (GULOSA) ===

def mochila_gulosa_fracionada(lista_valores, lista_pesos, capacidade_total):
    itens = [(v, p, v/p, i) for i, (v, p) in enumerate(zip(lista_valores, lista_pesos))]
    itens.sort(key=lambda x: x[2], reverse=True)
    valor_total, capacidade = 0, capacidade_total
    fracoes = [0] * len(lista_valores)
    for v, p, _, i in itens:
        if p <= capacidade:
            fracoes[i] = 1
            valor_total += v
            capacidade -= p
        else:
            fracoes[i] = capacidade / p
            valor_total += v * fracoes[i]
            break
    return valor_total, fracoes

valores = [60, 100, 120]
pesos = [10, 20, 30]
capacidade = 50
valor_final, composicao = mochila_gulosa_fracionada(valores, pesos, capacidade)

print("\nValor total carregado:", valor_final)
print("Frações utilizadas de cada item:", composicao)

plt.figure(figsize=(8, 5))
plt.bar(range(len(valores)), composicao, tick_label=[f"Item {i}" for i in range(len(valores))], color='orchid')
plt.title(f'Mochila Fracionária - Total: {valor_final:.2f}')
plt.ylim(0, 1.1)
for i, f in enumerate(composicao):
    plt.text(i, f + 0.03, f"{f*100:.1f}%", ha='center')
plt.tight_layout()
plt.show()

# === 6. SELEÇÃO DE ATIVIDADES (GULOSA + RECURSIVA) ===

def selecionar_agendamentos(inicios, finais):
    tarefas = sorted(zip(inicios, finais), key=lambda x: x[1])
    resultado, fim_ultimo = [], -1
    for ini, fim in tarefas:
        if ini >= fim_ultimo:
            resultado.append((ini, fim))
            fim_ultimo = fim
    return resultado

def selecionar_atividades_recursivamente(inicios, finais, fim_anterior=-1, i=0):
    if i >= len(inicios):
        return []
    if inicios[i] >= fim_anterior:
        return [(inicios[i], finais[i])] + selecionar_atividades_recursivamente(inicios, finais, finais[i], i+1)
    else:
        return selecionar_atividades_recursivamente(inicios, finais, fim_anterior, i+1)

inicios = [1, 3, 0, 5, 8, 5]
finais = [2, 4, 6, 7, 9, 9]
agendamento = selecionar_agendamentos(inicios, finais)

atividades_ord = sorted(zip(inicios, finais), key=lambda x: x[1])
inicios_ord, finais_ord = zip(*atividades_ord)
agendamento_rec = selecionar_atividades_recursivamente(inicios_ord, finais_ord)

print("\nAtividades selecionadas (iterativo):", agendamento)
print("Atividades selecionadas (recursivo):", agendamento_rec)

plt.figure(figsize=(10, 4))
for ini, fim in zip(inicios, finais):
    plt.barh(1, fim - ini, left=ini, height=0.4, color='lightgray')
for ini, fim in agendamento:
    plt.barh(1, fim - ini, left=ini, height=0.4, color='green')
plt.title("Agendamento Ótimo de Atividades (Guloso)")
plt.yticks([1], ["Agenda"])
plt.xlabel("Tempo")
plt.tight_layout()
plt.show()

# === 7. Problema do Troco Mínimo (Coin Change) ===

def coin_change_min_moedas(moedas, troco):
    dp = [float('inf')] * (troco + 1)
    dp[0] = 0
    for i in range(1, troco + 1):
        for m in moedas:
            if i - m >= 0:
                dp[i] = min(dp[i], dp[i - m] + 1)
    return dp

moedas = [1, 3, 4]
troco = 10
resultado_troco = coin_change_min_moedas(moedas, troco)

plt.figure(figsize=(8, 5))
plt.bar(range(troco + 1), resultado_troco, color='gold')
plt.title("💹 Troco Mínimo (Coin Change)")
plt.xlabel("Valor do Troco")
plt.ylabel("Número mínimo de moedas")
plt.tight_layout()
plt.show()

# === 8. Algoritmo de Dijkstra ===

def dijkstra(grafo, origem):
    distancias = {n: float('inf') for n in grafo.nodes}
    distancias[origem] = 0
    fila = [(0, origem)]
    predecessores = {}
    while fila:
        dist_atual, atual = heapq.heappop(fila)
        for vizinho in grafo[atual]:
            peso = grafo[atual][vizinho][0]['weight']
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                predecessores[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))
    return distancias, predecessores

dist_dijkstra, preds_dijkstra = dijkstra(rede_direcionada, 'x')
caminho = []
temp = 'y'
while temp != 'x':
    caminho.append((preds_dijkstra[temp], temp))
    temp = preds_dijkstra[temp]
caminho.reverse()

plt.figure()
nx.draw(rede_direcionada, posicoes_nos, with_labels=True, node_color='lightgreen', node_size=800)
nx.draw_networkx_edges(rede_direcionada, posicoes_nos, edgelist=caminho, edge_color='green', width=2)
plt.title("🧭 Caminho mais curto (Dijkstra de x a y)")
plt.tight_layout()
plt.show()

# === 9. Algoritmo A* ===

def heuristica(n1, n2):
    x1, y1 = posicoes_nos[n1]
    x2, y2 = posicoes_nos[n2]
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def a_estrela(grafo, inicio, objetivo):
    fila = [(0, inicio)]
    custos = {inicio: 0}
    pais = {}
    while fila:
        _, atual = heapq.heappop(fila)
        if atual == objetivo:
            break
        for vizinho in grafo[atual]:
            custo = grafo[atual][vizinho][0]['weight']
            novo_custo = custos[atual] + custo
            if vizinho not in custos or novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                prioridade = novo_custo + heuristica(vizinho, objetivo)
                heapq.heappush(fila, (prioridade, vizinho))
                pais[vizinho] = atual
    return pais

pais_astar = a_estrela(rede_direcionada, 'x', 'y')
cam_astar = []
temp = 'y'
while temp != 'x':
    cam_astar.append((pais_astar[temp], temp))
    temp = pais_astar[temp]
cam_astar.reverse()

plt.figure()
nx.draw(rede_direcionada, posicoes_nos, with_labels=True, node_color='lightcoral', node_size=800)
nx.draw_networkx_edges(rede_direcionada, posicoes_nos, edgelist=cam_astar, edge_color='red', width=2)
plt.title("Caminho A* de x a y")
plt.tight_layout()
plt.show()