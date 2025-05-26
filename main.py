from typing import List, Optional
import os

class Disciplina:
    def __init__(self, nome: str, carga_horaria: Optional[int] = None):
        self.nome = nome
        self.carga_horaria = carga_horaria

class DisciplinaCursada:
    def __init__(self, disciplina: Disciplina):
        self.disciplina = disciplina
        self.notas: List[float] = []

    def adicionar_nota(self, nota: float) -> bool:
        if len(self.notas) < 4 and 0 <= nota <= 10:
            self.notas.append(nota)
            return True
        return False

    def calcular_media(self) -> float:
        if self.notas:
            return sum(self.notas) / len(self.notas)
        return 0.0

class Aluno:
    def __init__(self, nome: str, matricula: str, serie: str, turma: str):
        self.nome = nome
        self.matricula = matricula
        self.serie = serie
        self.turma = turma
        self.disciplinas_cursadas: List[DisciplinaCursada] = []

    def adicionar_disciplina(self, disciplina: Disciplina) -> None:
        if not any(dc.disciplina.nome == disciplina.nome for dc in self.disciplinas_cursadas):
            self.disciplinas_cursadas.append(DisciplinaCursada(disciplina))

    def media_geral(self) -> float:
        medias = [d.calcular_media() for d in self.disciplinas_cursadas if d.notas]
        if medias:
            return sum(medias) / len(medias)
        return 0.0

    def situacao(self) -> str:
        return "Aprovado" if self.media_geral() >= 7.0 else "Reprovado"

class SistemaEscolar:
    def __init__(self):
        self.alunos: List[Aluno] = []
        self.disciplinas: List[Disciplina] = []

    def cadastrar_aluno(self, nome: str, matricula: str, serie: str, turma: str) -> None:
        if not any(a.matricula == matricula for a in self.alunos):
            self.alunos.append(Aluno(nome, matricula, serie, turma))
            print("Aluno cadastrado com sucesso!")
        else:
            print("Matrícula já existe!")

    def cadastrar_disciplina(self, nome: str, carga_horaria: Optional[int] = None) -> None:
        if not any(d.nome == nome for d in self.disciplinas):
            self.disciplinas.append(Disciplina(nome, carga_horaria))
            print("Disciplina cadastrada com sucesso!")
        else:
            print("Disciplina já existe!")

    def encontrar_aluno(self, matricula: str) -> Optional[Aluno]:
        return next((a for a in self.alunos if a.matricula == matricula), None)

    def encontrar_disciplina(self, nome: str) -> Optional[Disciplina]:
        return next((d for d in self.disciplinas if d.nome == nome), None)

    def lancar_nota(self, matricula: str, nome_disciplina: str, nota: float) -> None:
        aluno = self.encontrar_aluno(matricula)
        disciplina = self.encontrar_disciplina(nome_disciplina)

        if not aluno:
            print("Aluno não encontrado!")
            return
        if not disciplina:
            print("Disciplina não encontrada!")
            return

        aluno.adicionar_disciplina(disciplina)
        disciplina_cursada = next(dc for dc in aluno.disciplinas_cursadas if dc.disciplina.nome == nome_disciplina)
        
        if disciplina_cursada.adicionar_nota(nota):
            print("Nota lançada com sucesso!")
        else:
            print("Erro ao lançar nota! Verifique se já não atingiu o limite de 4 notas ou se a nota é válida.")

    def gerar_boletim(self, matricula: str) -> None:
        aluno = self.encontrar_aluno(matricula)
        if not aluno:
            print("Aluno não encontrado!")
            return

        print("\n" + "="*50)
        print(f"BOLETIM ESCOLAR - {aluno.nome}")
        print("="*50)
        print(f"Matrícula: {aluno.matricula}")
        print(f"Série: {aluno.serie}")
        print(f"Turma: {aluno.turma}")
        print("-"*50)

        for dc in aluno.disciplinas_cursadas:
            print(f"\nDisciplina: {dc.disciplina.nome}")
            print(f"Notas: {', '.join(map(str, dc.notas))}")
            print(f"Média: {dc.calcular_media():.1f}")

        print("\n" + "-"*50)
        print(f"Média Geral: {aluno.media_geral():.1f}")
        print(f"Situação: {aluno.situacao()}")
        print("="*50 + "\n")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    sistema = SistemaEscolar()
    
    while True:
        limpar_tela()
        print("\n=== SISTEMA DE GERENCIAMENTO ESCOLAR ===")
        print("1. Cadastrar Aluno")
        print("2. Cadastrar Disciplina")
        print("3. Lançar Nota")
        print("4. Gerar Boletim")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            nome = input("Nome completo: ")
            matricula = input("Matrícula: ")
            serie = input("Série: ")
            turma = input("Turma: ")
            sistema.cadastrar_aluno(nome, matricula, serie, turma)
            input("\nPressione Enter para continuar...")

        elif opcao == "2":
            nome = input("Nome da disciplina: ")
            carga = input("Carga horária (opcional, pressione Enter para pular): ")
            carga = int(carga) if carga.strip() else None
            sistema.cadastrar_disciplina(nome, carga)
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            matricula = input("Matrícula do aluno: ")
            nome_disciplina = input("Nome da disciplina: ")
            try:
                nota = float(input("Nota (0-10): "))
                sistema.lancar_nota(matricula, nome_disciplina, nota)
            except ValueError:
                print("Nota inválida!")
            input("\nPressione Enter para continuar...")

        elif opcao == "4":
            matricula = input("Matrícula do aluno: ")
            sistema.gerar_boletim(matricula)
            input("\nPressione Enter para continuar...")

        elif opcao == "5":
            print("\nSaindo do sistema...")
            break

        else:
            print("\nOpção inválida!")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    menu_principal() 