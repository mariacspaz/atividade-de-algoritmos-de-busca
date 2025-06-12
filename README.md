# atividade-de-algoritmos-de-busca
Fluxograma do Código Python 
Este fluxograma descreve a sequência de operações e as principais lógicas 
implementadas no script Python fornecido. 
Início do Programa 
1. Importações: 
○ Importa as bibliotecas networkx (para manipulação de grafos), matplotlib.pyplot 
(para visualização de gráficos) e heapq (para operações de fila de prioridade, 
usada em Dijkstra e A*). 
1. Criação e Visualização do Grafo 
1. Inicializar Grafo: 
○ Cria um grafo direcionado (nx.MultiDiGraph()). 
2. Adicionar Arestas: 
○ Adiciona arestas com pesos entre os nós definidos ('x', 'y', 'z', 'w'). 
3. Definir Coordenadas dos Nós: 
○ Define as posições ('coords_nos') para cada nó para a visualização. 
4. Desenhar Nós e Rótulos: 
○ Utiliza nx.draw_networkx_nodes e nx.draw_networkx_labels para desenhar os nós e 
seus rótulos. 
5. Desenhar Arestas e Pesos: 
○ Itera sobre as arestas para desenhá-las, ajustando o estilo para arestas 
múltiplas. 
○ Calcula a posição dos rótulos de peso nas arestas e os exibe usando plt.text. 
6. Configurar e Exibir Gráfico: 
○ Desativa os eixos (plt.axis('off')). 
○ Define o título do gráfico. 
○ Exibe o gráfico (plt.show()). 
2. Raízes e Folhas 
1. Definir Função encontrar_raizes_folhas: 
○ Recebe um grafo g como entrada. 
○ Identifica nós com grau de entrada zero (raízes) usando g.in_degree(). 
○ Identifica nós com grau de saída zero (folhas) usando g.out_degree(). 
○ Retorna as listas de nós iniciais e finais. 
2. Chamar Função: 
○ Chama encontrar_raizes_folhas com o grafo_dir. 
3. Imprimir Resultados: 
○ Exibe os "Nós de entrada" e "Nós de saída". 
3. Graus de Entrada e Saída 
1. Calcular Graus de Saída: 
○ Cria um dicionário graus_saida onde a chave é o nó e o valor é o seu grau de 
saída (grafo_dir.out_degree(n)). 
2. Calcular Graus de Entrada: 
○ Cria um dicionário graus_entrada onde a chave é o nó e o valor é o seu grau de 
entrada (grafo_dir.in_degree(n)). 
3. Imprimir Resultados: 
○ Exibe os dicionários de graus de saída e entrada. 
4. Caminhos e Ciclos 
1. Encontrar Caminhos Simples: 
○ Itera e imprime todos os caminhos simples de 'x' para 'y' usando 
nx.all_simple_paths. 
2. Verificar Acyclicidade: 
○ Verifica se o grafo é acíclico (nx.is_directed_acyclic_graph). 
○ Imprime "Sim" ou "Não" baseado no resultado. 
3. Detectar Ciclos: 
○ Tenta encontrar um ciclo usando nx.find_cycle. 
○ Se um ciclo for encontrado, imprime o ciclo. 
○ Se nenhuma exceção nx.NetworkXNoCycle for levantada (ou seja, não há ciclo), 
imprime "Sem ciclos detectados". 
5. Mochila Fracionária 
1. Definir Função mochila_fracionada: 
○ Recebe listas de valores, pesos e uma capacidade. 
○ Cria uma lista de itens com (valor, peso, razão_valor_peso, índice original). 
○ Ordena os itens em ordem decrescente pela razão valor/peso. 
○ Inicializa total = 0, resto = capacidade e fracoes (para armazenar a fração de cada 
item). 
○ Itera sobre os itens ordenados: 
■ Se o peso do item for menor ou igual ao resto da capacidade: 
■ Adiciona o item inteiro (fracoes[i] = 1), atualiza total e resto. 
■ Caso contrário (o item é muito pesado para ser adicionado inteiro): 
■ Adiciona uma fração do item (fracoes[i] = resto / p), atualiza total. 
■ Sai do loop. 
○ Retorna o total de lucro e as fracoes de cada item. 
2. Definir Dados e Chamar Função: 
○ Define lucros, pesagens e cap_limite. 
○ Chama mochila_fracionada. 
3. Imprimir Resultados: 
○ Exibe o "Lucro total" e as "Frações por item". 
4. Plotar Resultados: 
○ Cria um gráfico de barras (plt.bar) mostrando a fração utilizada de cada item. 
○ Define título, limites do eixo Y e rótulos de porcentagem. 
○ Exibe o gráfico (plt.show()). 
6. Seleção de Atividades 
1. Definir Função Iterativa agendar_atividades: 
○ Recebe listas de inicio_lst e fim_lst. 
○ Combina e ordena os eventos pelo tempo de término. 
○ Inicializa agenda e fim_ant. 
○ Itera sobre os eventos ordenados: 
■ Se o tempo de início do evento atual for maior ou igual ao fim_ant: 
■ Adiciona o evento à agenda e atualiza fim_ant. 
○ Retorna a agenda. 
2. Definir Função Recursiva agendar_recursivo: 
○ Recebe ini_lst, fim_lst, fim_ant (com padrão -1) e i (com padrão 0). 
○ Base Case: Se i for maior ou igual ao comprimento da lista, retorna uma lista 
vazia. 
○ Recursive Step: 
■ Se ini_lst[i] for maior ou igual a fim_ant: 
■ Retorna o evento atual concatenado com a chamada recursiva para o 
próximo evento. 
■ Caso contrário: 
■ Retorna a chamada recursiva para o próximo evento (ignorando o 
atual). 
3. Definir Dados e Chamar Funções: 
○ Define iniciais e finais. 
○ Chama agendar_atividades (iterativa). 
○ Prepara os dados para a versão recursiva (ordenando). 
○ Chama agendar_recursivo. 
4. Imprimir Resultados: 
○ Exibe a "Agenda (iterativa)" e a "Agenda (recursiva)". 
5. Plotar Resultados: 
○ Cria um gráfico de barras horizontais, mostrando todas as atividades em 
cinza e as atividades agendadas em verde. 
○ Define título, rótulos e eixos. 
○ Exibe o gráfico (plt.show()). 
7. Troco Mínimo 
1. Definir Função troco_minimo: 
○ Recebe moedas_disp (moedas disponíveis) e valor (valor a ser trocado). 
○ Cria uma lista dp (programação dinâmica) de tamanho valor + 1, inicializada 
com infinito. 
○ dp[0] é definido como 0 (0 moedas para fazer troco de 0). 
○ Itera de 1 até valor (inclusive valor): 
■ Para cada moeda em moedas_disp: 
■ Se i - moeda for maior ou igual a 0: 
■ Atualiza dp[i] com o mínimo entre o valor atual e dp[i - moeda] + 1. 
○ Retorna a lista dp. 
2. Definir Dados e Chamar Função: 
○ Define moedas_entrada e valor_troco. 
○ Chama troco_minimo. 
3. Plotar Resultados: 
○ Cria um gráfico de barras (plt.bar) mostrando a quantidade mínima de moedas 
para cada valor de 0 até valor_troco. 
○ Define título, rótulos dos eixos. 
○ Exibe o gráfico (plt.show()). 
8. Dijkstra 
1. Definir Função menor_caminho_dijkstra: 
○ Recebe um grafo g e um nó inicio. 
○ Inicializa dist (dicionário de distâncias para infinito, com dist[inicio] = 0). 
○ Cria uma fila de prioridade (usando heapq) com (0, inicio). 
○ Inicializa anterior (dicionário para reconstruir o caminho). 
○ Loop while fila: 
■ Retira o nó com a menor distância da fila. 
■ Para cada vizinho do nó atual: 
■ Calcula o peso da aresta. 
■ Calcula a nova_dist. 
■ Se nova_dist for menor que a distância registrada para o vizinho: 
■ Atualiza dist[viz]. 
■ Define anterior[viz] como o nó atual. 
■ Adiciona (nova_dist, viz) à fila. 
○ Retorna dist e anterior. 
2. Chamar Função: 
○ Chama menor_caminho_dijkstra com grafo_dir e 'x'. 
3. Reconstruir Caminho: 
○ Inicia do nó 'y' e volta até 'x' usando o dicionário caminhos_x (anterior). 
○ Armazena as arestas do caminho em trajeto. 
○ Inverte trajeto. 
4. Plotar Caminho: 
○ Desenha o grafo completo. 
○ Desenha as arestas do trajeto em verde para destacá-lo. 
○ Define o título. 
○ Exibe o gráfico (plt.show()). 
9. A* 
1. Definir Função distancia_heuristica: 
○ Recebe dois nós a e b. 
○ Calcula a distância euclidiana entre as coordenadas dos nós. 
○ Retorna a distância. 
2. Definir Função caminho_a_estrela: 
○ Recebe um grafo g, um nó ini e um nó alvo. 
○ Inicializa fila de prioridade com (0, ini). 
○ Inicializa custos (dicionário para armazenar o custo do caminho do início até 
cada nó). 
○ Inicializa pais (dicionário para reconstruir o caminho). 
○ Loop while fila: 
■ Retira o nó com menor prioridade da fila. 
■ Se o nó atual for o alvo, sai do loop. 
■ Para cada vizinho do nó atual: 
■ Calcula o peso da aresta. 
■ Calcula o novo_custo do início até o vizinho. 
■ Se o vizinho não estiver em custos ou novo_custo for menor que 
custos[viz]: 
■ Atualiza custos[viz]. 
■ Calcula prioridade (novo_custo + distancia_heuristica(viz, alvo)). 
■ Adiciona (prioridade, viz) à fila. 
■ Define pais[viz] como o nó atual. 
○ Retorna o dicionário pais. 
3. Chamar Função: 
○ Chama caminho_a_estrela com grafo_dir, 'x' e 'y'. 
4. Reconstruir Caminho: 
○ Inicia do nó 'y' e volta até 'x' usando o dicionário pais_estrela. 
○ Armazena as arestas do caminho em trajeto_astar. 
○ Inverte trajeto_astar. 
5. Plotar Caminho: 
○ Desenha o grafo completo. 
○ Desenha as arestas do trajeto_astar em vermelho para destacá-lo. 
○ Define o título. 
○ Exibe o gráfico (plt.show()). 
Fim do Programa 
