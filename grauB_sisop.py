# Feito por Bernardo Salvador. Criado em VScode Windows 11, Python 3.13.7. Correções de erros e verificação de sintaxe feita no ChatGPT 5.3

import random
import time

# ------------------------------
# CONFIGURAÇÕES DO SISTEMA
# ------------------------------

PAGE_SIZE = 8 * 1024  # 8 KB
VIRTUAL_MEMORY_SIZE = 1 * 1024 * 1024  # 1 MB
PHYSICAL_MEMORY_SIZE = 64 * 1024  # 64 KB

NUM_PAGES = VIRTUAL_MEMORY_SIZE // PAGE_SIZE  # 128
NUM_FRAMES = PHYSICAL_MEMORY_SIZE // PAGE_SIZE  # 8

# ------------------------------
# ESTRUTURAS
# ------------------------------

class PageTableEntry:
    def __init__(self):
        self.frame = None
        self.present = False
        self.last_used = 0


class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size
        self.num_pages = (size + PAGE_SIZE - 1) // PAGE_SIZE

        # tabela de páginas
        self.page_table = [PageTableEntry() for _ in range(self.num_pages)]

        # memória virtual (dados simulados)
        self.virtual_memory = {}
        for page in range(self.num_pages):
            self.virtual_memory[page] = f"Dados(P{pid}-Pag{page})"

    def generate_address(self):
        return random.randint(0, self.size - 1)


class PhysicalMemory:
    def __init__(self):
        self.frames = [None] * NUM_FRAMES  # cada frame guarda dados reais

    def get_free_frame(self):
        for i, frame in enumerate(self.frames):
            if frame is None:
                return i
        return None

    def show_memory(self):
        print("\n=== MEMÓRIA FÍSICA ===")
        for i, frame in enumerate(self.frames):
            print(f"Frame {i}: {frame}")


# ------------------------------
# MMU
# ------------------------------

class MMU:
    def __init__(self, memory, processes):
        self.memory = memory
        self.processes = processes
        self.time = 0

    def executar_instrucao(self, process, virtual_address):
        self.time += 1

        print("\n==============================")
        print(f"[CPU] Nova instrução: Processo {process.pid} acessa {virtual_address}")

        # 1. Gerar endereço virtual
        page = virtual_address // PAGE_SIZE
        offset = virtual_address % PAGE_SIZE

        print(f"[MMU] Endereço virtual → Página {page}, Offset {offset}")

        # 2. Consultar tabela de páginas
        entry = process.page_table[page]

        # 3. Verificar presença
        if entry.present:
            print("[MMU] Página presente na memória")

            entry.last_used = self.time
            frame = entry.frame

        else:
            print("[MMU] >>> FALTA DE PÁGINA <<<")
            frame = self.tratar_page_fault(process, page)

        # 4. Traduzir endereço
        physical_address = frame * PAGE_SIZE + offset
        print(f"[MMU] Endereço físico: {physical_address}")

        # 5. Apresentar conteúdo
        content = self.memory.frames[frame]["data"]
        print(f"[SAÍDA] Conteúdo acessado: {content}")

    def tratar_page_fault(self, process, page):
        print("[MMU] Tratando falta de página...")

        free_frame = self.memory.get_free_frame()

        # Caso 1: existe frame livre
        if free_frame is not None:
            print(f"[MMU] Frame livre encontrado: {free_frame}")
            frame = free_frame

        # Caso 2: precisa substituir
        else:
            print("[MMU] Sem frames livres → aplicando LRU")
            frame = self.substituir_pagina()

        # carregar página da memória virtual
        data = process.virtual_memory[page]

        self.memory.frames[frame] = {
            "pid": process.pid,
            "page": page,
            "data": data
        }

        entry = process.page_table[page]
        entry.frame = frame
        entry.present = True
        entry.last_used = self.time

        print(f"[MMU] Página {page} carregada no frame {frame}")

        return frame

    def substituir_pagina(self):
        oldest_time = float('inf')
        victim_frame = None
        victim_entry = None

        for i, frame in enumerate(self.memory.frames):
            pid = frame["pid"]
            page = frame["page"]

            proc = next(p for p in self.processes if p.pid == pid)
            entry = proc.page_table[page]

            if entry.last_used < oldest_time:
                oldest_time = entry.last_used
                victim_frame = i
                victim_entry = entry
                victim_pid = pid
                victim_page = page

        print(f"[MMU] Substituindo página {victim_page} do processo {victim_pid}")

        victim_entry.present = False
        victim_entry.frame = None

        return victim_frame


# ------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------

def mostrar_tabela(process):
    print(f"\n--- TABELA DE PÁGINAS (Processo {process.pid}) ---")
    for i, entry in enumerate(process.page_table):
        print(f"Página {i}: Frame={entry.frame} | Presente={entry.present}")


# ------------------------------
# SIMULAÇÃO
# ------------------------------

# Criar processos
processes = [
    Process(1, 300000),
    Process(2, 700000)
]

memory = PhysicalMemory()
mmu = MMU(memory, processes)

# Executar simulação
for _ in range(15):
    proc = random.choice(processes)
    addr = proc.generate_address()

    mmu.executar_instrucao(proc, addr)

    mostrar_tabela(proc)
    memory.show_memory()

    time.sleep(0.5)