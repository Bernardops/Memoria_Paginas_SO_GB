# Memoria_Paginas_SO_GB
# Feito por: Bernardo Petry Salvador.
# Grau B na cadeira de Sistemas Operacionais: Análise e Aplicações

# Simulador de Memória Virtual com Paginação

Este projeto implementa um simulador de gerenciamento de memória baseado em paginação, reproduzindo o funcionamento de uma MMU (Memory Management Unit) em um sistema fictício.

O objetivo é demonstrar, de forma prática, como ocorre a tradução de endereços virtuais para físicos, incluindo o tratamento de faltas de página (page fault) e a substituição de páginas na memória principal.

---

## Configuração do Sistema

- Memória virtual: 1 MB  
- Memória principal: 64 KB  
- Tamanho de página/frame: 8 KB  
- Total de páginas virtuais: 128  
- Total de frames: 8  
- Múltiplos processos leves simulados  

---

## Funcionamento

O simulador segue o fluxo clássico de acesso à memória:

1. Um processo gera um endereço virtual  
2. A MMU divide o endereço em página e offset  
3. Consulta a tabela de páginas  
4. Se a página estiver na memória:
   - o acesso é feito diretamente  
5. Caso contrário:
   - ocorre page fault  
   - a página é carregada em um frame livre ou substitui outra (LRU)  
6. O endereço físico é gerado e o conteúdo é exibido  

---

## Principais Componentes

- Processo: possui espaço de memória virtual e tabela de páginas  
- MMU: responsável pela tradução de endereços  
- Memória Física: composta por frames  
- Tabela de Páginas: controla presença e mapeamento  
- Substituição de Páginas: algoritmo LRU (Least Recently Used)  

---

## Saída do Programa

Durante a execução, o simulador exibe:

- Endereço virtual acessado  
- Tradução para endereço físico  
- Ocorrência de page fault  
- Substituição de páginas, quando necessário  
- Conteúdo acessado  
- Estado da memória e das tabelas  

---  
