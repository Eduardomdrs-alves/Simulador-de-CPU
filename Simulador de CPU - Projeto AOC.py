class CPU:
    def __init__(self, memoria_tamanho=64):
        self.memoria = [0] * memoria_tamanho
        self.registradores = {'R0': 0, 'R1': 0, 'R2': 0}
        self.PC = 0
        self.instrucoes = []

    def carregar_programa(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha == "" or linha.startswith("#"):
                    continue
                self.instrucoes.append(linha)

    def buscar_instrução(self):
        if self.PC < len(self.instrucoes):
            return self.instrucoes[self.PC]
        return None

    def decodificar_executar(self, instrucao):
        partes = instrucao.split()
        comando = partes[0]

        if comando == "HLT":
            return False

        elif comando == "LOAD":
            reg, valor = partes[1].strip(','), partes[2]
            if valor.startswith('['):  # Carregando da memória
                endereco = int(valor.strip('[]'))
                self.registradores[reg] = self.memoria[endereco]
            else:  # Valor imediato
                self.registradores[reg] = int(valor)

        elif comando == "STORE":
            endereco, reg = partes[1].strip(','), partes[2]
            endereco = int(endereco.strip('[]'))
            self.memoria[endereco] = self.registradores[reg]

        elif comando == "ADD":
            reg1, reg2 = partes[1].strip(','), partes[2]
            self.registradores[reg1] += self.registradores[reg2]

        else:
            print(f"Instrução desconhecida: {instrucao}")

        return True

    def executar(self):
        while True:
            instrucao = self.buscar_instrução()
            if instrucao is None:
                break
            print(f"\nPC: {self.PC} | Executando: {instrucao}")
            continuar = self.decodificar_executar(instrucao)
            self.PC += 1
            self.estado()
            if not continuar:
                break

    def estado(self):
        print("Registradores:", self.registradores)
        print("PC:", self.PC)
        print("Memória (não vazia):")
        for i, val in enumerate(self.memoria):
            if val != 0:
                print(f"  [{i}] = {val}")

# Uso
if __name__ == "__main__":
    cpu = CPU()
    cpu.carregar_programa("exemplo.txt")  # Substitua pelo caminho do seu programa
    cpu.executar()
