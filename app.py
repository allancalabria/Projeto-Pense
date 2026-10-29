from flask import Flask, render_template, request, redirect, url_for, flash
import models

m1 = models.Trabalho("Jurassic Park", "Machado de Assis", "Aventura")
m2 = models.Trabalho("Água da Pedra", "Arnold Shwazneeger", "Aventura")
m3 = models.Trabalho("Mundo dos macacos", "José Lins do Rego", "Simulador")
m4 = models.Trabalho("Automobilista", "Max Verstappen", "Corrida")

app = Flask(__name__)
app.secret_key = "chave_secreta_para_o_flash_funcionar"

# Lista global temporária (simulação de banco de dados na memória do servidor)
# Já iniciada com um exemplo para fins de testes no seu Dashboard
trabalhos = [
    {
        "titulo": "Desenvolvimento do Sistema PEnsE-Submite",
        "autor": "Grupo Front-end e Back-end",
        "instituicao": "IFRS - Campus Farroupilha",
        "modalidade": "Ensino",
        "resumo": "Protótipo inicial para simular a submissão de resumos da Jornada Científica."
    }
]

# Rota do Dashboard (Página Inicial)
@app.route('/')
def dashboard():
    # Passa a lista global de trabalhos para o template HTML
    return render_template('dashboard.html', trabalhos=trabalhos)


# Rota do Formulário Corrigida
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # 1. Captura os dados enviados pelo formulário HTML através do atributo 'name'
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        instituicao = request.form.get('instituicao')
        modalidade = request.form.get('modalidade')
        resumo = request.form.get('resumo')
        
        # 2. Validação simples: garante que nenhum campo veio em branco
        if titulo and autor and instituicao and modalidade and resumo:
            # Cria um dicionário com os dados do novo trabalho
            novo_trabalho = {
                "titulo": titulo,
                "autor": autor,
                "instituicao": instituicao,
                "modalidade": modalidade,
                "resumo": resumo
            }
            # 3. Adiciona o dicionário na lista global
            trabalhos.append(novo_trabalho)
            
            # Mensagem de sucesso (opcional, mas boa prática)
            flash("Trabalho submetido com sucesso!", "success")
            
            # 4. Redireciona o usuário imediatamente para a página inicial (Dashboard)
            return redirect(url_for('dashboard'))
        
        # Caso falte algum campo, exibe erro e recarrega o formulário
        flash("Erro: Preencha todos os campos obrigatórios!", "danger")
        return redirect(url_for('form'))    
        
    # Se o método for GET, apenas exibe a página do formulário
    # Certifique-se de que o nome do arquivo aqui bate com o seu arquivo HTML (ex: enviar.html)
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
