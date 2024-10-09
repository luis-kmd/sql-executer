import sys
from PySide6.QtWidgets import QApplication, QDialog, QTextEdit, QTabWidget, QPushButton, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QColor, QBrush, QIcon
from PySide6.QtGui import QTextCharFormat, QSyntaxHighlighter
from PySide6.QtCore import Qt
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QTableView, QLabel, QScrollArea
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QThread, Signal
from tela_ui import Ui_Dialog
from datetime import datetime
import requests
import keyboard
import pandas as pd

QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Classe para alterar cores de palavras chave
class SqlHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Formato para palavras reservadas
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(Qt.blue)  # Azul 

        # Formato para strings
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(Qt.red)  # Vermelho 

        # Formato para ligacoes
        self.join_format = QTextCharFormat()
        self.join_format.setForeground(Qt.gray)  # Cinza 

        # Formato para alteracoes
        self.alter_format = QTextCharFormat()
        self.alter_format.setForeground(QColor("#FF007F"))  # Rosa 

        # Formato para comentarios
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(Qt.darkGreen)  # Verde

        # Lista de palavras relacionadas a ligacoes
        self.joinwords = ["JOIN", "INNER", "LEFT", "RIGHT", "OUTER", "LIKE", "AND", "OR", "NULL", "EXISTS", "IN", "NOT", "BETWEEN", "IS", "NOT"]

        self.alterwords = ["CAST", "SUM", "MAX", "AVG", "UPDATE", "CONCAT"]

        # Lista de palavras reservadas em SQL
        self.keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "DELETE", "GROUP", "ORDER",
            "BY", "HAVING", "AS", "DISTINCT", "CREATE", "ALTER", "DROP",
            "INDEX", "TABLE", "PRIMARY", "FOREIGN", "KEY", "UNION", 
            "EXISTS", "AS", "ASC", "DESC", "TOP", "VALUES", "INTO", "SET", "PROCEDURE", "VIEW", "IF", "ELSE", "BEGIN", "END", "RETURN", "WHILE", "DECLARE", "CURSOR", "OPEN", "FETCH", "CLOSE", "DEALLOCATE", "FETCH", "NEXT", "INTO", "EXEC", "EXECUTE", "PRINT", "RAISEERROR", "TRY", "CATCH", "TRANSACTION", "COMMIT", "ROLLBACK",
            "CASE", "WHEN", "THEN"
        ]

        # Regras de realce
        self.highlighting_rules = []

        # Adiciona regras para palavras de alteracao
        for alter in self.alterwords:
            pattern = QRegularExpression(r'\b' + alter + r'\b') # Adiciona limites de palavra
            self.highlighting_rules.append((pattern, self.alter_format))

        # Adiciona regras para palavras reservadas
        for keyword in self.keywords:
            pattern = QRegularExpression(r'\b' + keyword + r'\b')  # Adiciona limites de palavra
            self.highlighting_rules.append((pattern, self.keyword_format))

        # Adiciona regras para palavras relacionadas a ligacoes
        for join in self.joinwords:
            pattern = QRegularExpression(r'\b' + join + r'\b')  # Adiciona limites de palavra
            self.highlighting_rules.append((pattern, self.join_format))

        # Adiciona regras para strings (valores entre aspas simples)
        self.highlighting_rules.append((QRegularExpression(r"'[^']*'"), self.string_format))

        # Adiciona regras para comentários (a partir de '--')
        self.highlighting_rules.append((QRegularExpression(r'--.*'), self.comment_format))

    def highlightBlock(self, text: str):
        text_upper = text.upper()  

        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text_upper)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start, length = match.capturedStart(), match.capturedLength()
                self.setFormat(start, length, fmt)

        self.setCurrentBlockState(0)

        
class ApiThread(QThread):
    data_ready = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, metodo, query):
        super().__init__()
        self.metodo = metodo
        self.query = query

    def run(self):
        try:
            # Acessando o banco de dados a ser utilizado com api
            url = 'ADRESS'
            auth = ('USER', 'PASS')
            headers = {'Content-Type': 'application/json'}
            payload = {'query': self.query}
            
            # Imprime a query para debug
            print(f"Enviando query: {self.query}")
            
            # Verifica o método de envio
            if self.metodo == 'GET':
                url = f"{url}/consulta"
                response = requests.get(url, headers=headers, auth=auth, json=payload)
            elif self.metodo == 'POST':
                url = f"{url}/executar"
                response = requests.post(url, headers=headers, auth=auth, json=payload)
            else:
                return
            
            # Verifica se o status da resposta é 200 (sucesso)
            if response.status_code == 200:
                # Tenta capturar o JSON, mas se falhar, apenas exibe mensagem de sucesso
                try:
                    data = response.json()
                    self.data_ready.emit(data)
                except ValueError:
                    # Resposta não é JSON (caso de criação de views ou procedures)
                    self.data_ready.emit([{"status": "Comando executado com sucesso."}])
            else:
                # Mostra o erro com o status code e a mensagem de erro da API
                self.error_occurred.emit(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            # Emite o erro caso ocorra alguma exceção no processo
            self.error_occurred.emit(str(e))


class Sql(QDialog):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.ui = Ui_Dialog()  # Inicialize a interface gerada
        self.ui.setupUi(self)  # Configura a interface

        # Define o tamanho fixo 
        fixed_width = 1220
        fixed_height = 860
        self.setFixedSize(fixed_width, fixed_height)

        self.show()

        self.setWindowTitle("SQL Execute")

        self.icon = QIcon('KMD.png')
        self.setWindowIcon(self.icon)

        # Definindo os campos
        self.query_text = self.ui.CodigosSQL
        self.tab_widget = self.ui.Tabela

        # Definindo os botões
        self.botaoExportar = self.ui.exportarExcel
        self.botaoQuery = self.ui.botaoConsultar
        self.botaoCancelar = self.ui.botaoCancelar
        self.botaocopy = self.ui.botaoCopiar

        # Criar QScrollArea para a tabela
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Para que o scroll ajuste conforme o tamanho do conteúdo

        # Criar QTableView dentro da QScrollArea
        self.table_view = QTableView(self.scroll_area)
        self.scroll_area.setWidget(self.table_view)  # Define o QTableView como o widget da QScrollArea
        
        # Adiciona a QScrollArea como uma aba
        self.tab_widget.addTab(self.scroll_area, "Resultados da Consulta")

        # Criar QLabel para mensagens
        self.message_label = QLabel(self)
        self.tab_widget.addTab(self.message_label, "Mensagens")

        # Aplicar o highlighter no QTextEdit
        self.highlighter = SqlHighlighter(self.query_text.document())

        # Inicialmente, ocultamos o QTabWidget
        self.tab_widget.hide()

        # Conectar o botão à função de consulta e exportação
        self.botaoQuery.clicked.connect(self.consultar)
        self.botaoCancelar.clicked.connect(self.close)
        self.botaoExportar.clicked.connect(self.exportar_para_excel)
        self.botaocopy.clicked.connect(self.copiar_dados)

        # Atalho para executar a consulta com f5
        keyboard.add_hotkey('f5', self.consultar)

        # Dados da consulta (armazenados após a consulta)
        self.dados_consulta = []

        # VISUAL

        self.botaoQuery.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #32CD32;
            }
        """)

        self.botaoExportar.setStyleSheet("""
            QPushButton {
                background-color: #6495ED;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #87CEFA;
            }
        """)

        self.botaocopy.setStyleSheet("""
            QPushButton {
                background-color: #6495ED;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #87CEFA;
            }
        """)

        self.botaoQuery.setIcon(QIcon('play.png'))
        self.botaoExportar.setIcon(QIcon('export.png'))
        self.botaocopy.setIcon(QIcon('copiar.png'))
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
            }
        """)

    def close(self):
        self.thread.terminate()

    def consultar(self):
        self.tab_widget.show()

        # exibe o texto da consulta
        query = self.query_text.toPlainText()
        print("Consulta executada:", query)

        # Verifica se é um comando para criar uma view ou procedure
        if query.strip().upper().startswith("CREATE VIEW") or query.strip().upper().startswith("CREATE PROCEDURE"):
            # Para criação de views ou procedures, use POST
            self.thread = ApiThread('POST', query)
        else:
            # Para consultas e outros comandos, use GET
            self.thread = ApiThread('GET', query)

        self.thread.data_ready.connect(self.popular_tabela)
        self.thread.error_occurred.connect(self.mostrar_erro)
        self.tab_widget.setCurrentIndex(1)
        self.thread.start()

    def formatar_data(self, data_str):
        # Define o formato da string que você está recebendo
        formato_original = "%a, %d %b %Y %H:%M:%S %Z"
        # Converte a string para um objeto datetime
        data_obj = datetime.strptime(data_str, formato_original)
        # Retorna a data no formato desejado
        return data_obj.strftime('%Y-%m-%d')

    def popular_tabela(self, dados):
        # Debug para verificar o conteúdo dos dados recebidos
        print(f"Dados recebidos: {dados}")
        
        # Verifica se a consulta retornou dados ou se foi um comando DDL (como CREATE VIEW/PROCEDURE)
        if not dados or (isinstance(dados, list) and 'status' in dados[0]):
            # Caso seja um comando sem dados retornados (como CREATE VIEW/PROCEDURE)
            status_message = dados[0].get('status', 'Comando executado com sucesso.') if dados else 'Comando executado com sucesso.'
            self.message_label.setText(status_message)
            return

        self.dados_consulta = dados  # Armazena os dados para exportação
        model = QStandardItemModel()
        
        # Define os cabeçalhos a partir das chaves do primeiro dicionário
        model.setHorizontalHeaderLabels(dados[0].keys())  
        for linha in dados:
            items = []
            for chave, valor in linha.items():
                # Verifica se o valor é uma string que parece uma data
                if isinstance(valor, str) and "GMT" in valor:
                    valor = self.formatar_data(valor)  # Formata a data

                if valor is None:
                    valor = "NULL"  # Substitui None por NULL
                    item = QStandardItem(valor)
                    item.setBackground(QBrush(QColor(255, 255, 204)))  # Amarelo claro para o fundo
                else:
                    item = QStandardItem(str(valor))
                items.append(item)
            model.appendRow(items)

        self.table_view.setModel(model)

        # Ajustar a largura das colunas
        for i in range(model.columnCount()):
            self.table_view.setColumnWidth(i, 100) 

        # Ativar rolagem horizontal
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Mostra a barra de rolagem apenas quando necessário

        if len(dados) == 1:
            self.message_label.setText("Consulta executada com sucesso.\n1 linha afetada.")
        else:
            self.message_label.setText(f"Consulta executada com sucesso.\n{len(dados)} linhas afetadas.")
        self.tab_widget.setTabIcon(1, QIcon('sucess.png')) 
        self.tab_widget.setCurrentIndex(0)


    def mostrar_erro(self, mensagem):
        self.tab_widget.setTabIcon(1, QIcon('error.png'))  # Ícone para a aba de mensagens
        self.tab_widget.setCurrentIndex(1)
        self.message_label.setText(f"Erro: {mensagem}")

    def exportar_para_excel(self):
        # Verifica se há dados para exportar
        if not self.dados_consulta:
            self.message_label.setText("Nenhum dado para exportar.")
            return

        # Solicita ao usuário o caminho e o nome do arquivo
        caminho_arquivo, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Arquivos Excel (*.xlsx)")
        if not caminho_arquivo:
            return  # O usuário cancelou o diálogo

        # Prepara os dados para exportação, tratando NULLs e formatando datas
        dados_exportar = []
        for linha in self.dados_consulta:
            linha_exportar = {}
            for chave, valor in linha.items():
                # Verifica se o valor é uma string que parece uma data
                if isinstance(valor, str) and "GMT" in valor:
                    valor = self.formatar_data(valor)  # Formata a data

                # Substitui None por "NULL" para manter consistência
                if valor is None:
                    valor = "NULL"
                    
                linha_exportar[chave] = valor

            dados_exportar.append(linha_exportar)

        try:
            # Converte os dados para um DataFrame do pandas
            df = pd.DataFrame(dados_exportar)

            # Exporta os dados para um arquivo Excel
            df.to_excel(caminho_arquivo, index=False)

            self.message_label.setText(f"Dados exportados com sucesso para {caminho_arquivo}.")
        except Exception as e:
            self.message_label.setText(f"Erro ao exportar: {str(e)}")

    def copiar_dados(self):
        # Verifica se há dados para copiar
        model = self.table_view.model()
        if not model:
            self.message_label.setText("Nenhum dado para copiar.")
            return

        # Prepara os dados da tabela para copiar
        clipboard_data = []
        
        # Cabeçalhos das colunas
        headers = [model.horizontalHeaderItem(i).text() for i in range(model.columnCount())]
        clipboard_data.append("\t".join(headers))  # Adiciona os cabeçalhos separados por tabulação
        
        # Linhas de dados
        for row in range(model.rowCount()):
            linha = []
            for col in range(model.columnCount()):
                item = model.item(row, col)
                valor = item.text() if item else "NULL"
                linha.append(valor)
            clipboard_data.append("\t".join(linha))  # Adiciona as linhas separadas por tabulação

        # Junta tudo em uma única string, com quebras de linha entre cada linha
        dados_formatados = "\n".join(clipboard_data)
        
        # Copia os dados para a área de transferência
        clipboard = QApplication.clipboard()
        clipboard.setText(dados_formatados)
        self.tab_widget.setCurrentIndex(1)
        self.message_label.setText("Dados copiados para a área de transferência.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Sql()
    sys.exit(app.exec())
