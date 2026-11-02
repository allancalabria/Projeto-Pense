# 🎓 PEnsE - Trabalhos Acadêmicos

> 🚀 **Acesse a aplicação em produção:**
>
> ### 🔗 **[https://projeto-pense.onrender.com/](https://projeto-pense.onrender.com/)**
>
> [![Status](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://projeto-pense.onrender.com/)
> [![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
> [![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

---

## 📖 Sobre o Projeto

O **PEnsE (Trabalhos Acadêmicos)** é uma plataforma web desenvolvida para centralizar a submissão, organização e divulgação de trabalhos, pesquisas e projetos acadêmicos nas modalidades de **Ensino**, **Pesquisa** e **Extensão**.

A aplicação oferece um ambiente intuitivo para que autores e estudantes submetam seus resumos científicos, visualizem publicações recentes em formato de cards interativos e contem com uma interface moderna e responsiva. Como diferencial criativo, o projeto inclui uma experiência interativa com mini-game em pixel art integrado ao plano de fundo.

---

## ✨ Funcionalidades

- **📋 Dashboard Acadêmico:**

  - Listagem dos trabalhos cadastrados em formato de cards informativos.
  - Exibição de categoria/modalidade (Ensino, Pesquisa, Extensão), título, autor principal, instituição de ensino e resumo.
  - Estado vazio estilizado caso nenhum trabalho tenha sido submetido ainda.
- **✍️ Formulário de Submissão:**

  - Cadastro simplificado com campos para: Título, Autor, Instituição, Modalidade e Resumo.
  - Validação de preenchimento obrigatório de todos os campos.
  - Notificações dinâmicas (flash messages) informando o sucesso ou erro da operação.
- **💾 Banco de Dados Híbrido:**

  - Execução automática em **SQLite** para desenvolvimento local simplificado.
  - Suporte e adaptação nativa para **PostgreSQL** em ambiente de produção (Render).
- **🎮 Easter Egg / Mini-Game Interativo:**

  - Camada de entretenimento visual com sprites em pixel art integrada no background das páginas.
  - Seleção de pilotos, movimentação de aeronaves, lançamento de alvos e sistema de pontuação persistente via módulos JavaScript (ES6).

---

## 🛠️ Tecnologias Utilizadas

### **Backend**

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/) - Microframework web
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) & [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para manipulação do banco de dados
- [Gunicorn](https://gunicorn.org/) - Servidor WSGI para produção
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Gerenciamento de variáveis de ambiente
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) - Driver PostgreSQL

### **Frontend**

- [Jinja2](https://palletsprojects.com/p/jinja/) - Motor de templates
- [Tailwind CSS v4](https://tailwindcss.com/) - Framework utilitário de estilização
- [Iconoir](https://iconoir.com/) - Biblioteca de ícones open-source
- HTML5, CSS3 e JavaScript Moderno (ES Modules)

### **Infraestrutura e Deploy**

- [Render](https://render.com/) - Hospedagem da aplicação web e do banco PostgreSQL

---

## 📁 Estrutura de Diretórios

```text
Projeto-Pense/
├── models/
│   ├── __init__.py        # Exportação dos modelos
│   └── Trabalho.py        # Modelo SQLAlchemy da entidade Trabalho
├── static/
│   ├── css/
│   │   └── style.css      # Estilização complementar e variáveis visuais
│   ├── img/
│   │   └── sprites/       # Spritesheets e imagens pixel art
│   └── js/
│       ├── game/          # Módulos do mini-game (Plane, Bomb, Target, Game, etc.)
│       └── game.js
├── templates/
│   ├── base.html          # Template base com navbar, alertas e background
│   ├── dashboard.html     # Página inicial com cards dos trabalhos
│   └── form.html          # Página de cadastro/submissão de trabalho
├── instance/              # Banco SQLite local (criado automaticamente)
├── .env.example           # Modelo de variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo controle de versão
├── app.py                 # Ponto de entrada da aplicação e definição de rotas
├── config.py              # Configuração do banco de dados e chave de sessão
├── requirements.txt       # Dependências Python do projeto
└── tailwind.config.js     # Configuração de temas do Tailwind
```

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos

- **Python 3.10+** instalado
- **Git** instalado

### Passo a Passo

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/allancalabria/Projeto-Pense.git
   cd Projeto-Pense
   ```
2. **Crie e ative um ambiente virtual:**

   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto a partir do exemplo:

   ```bash
   cp .env.example .env
   ```

   *Conteúdo recomendado para ambiente local:*

   ```ini
   SECRET_KEY=sua_chave_secreta_aqui
   # DATABASE_URL é opcional no ambiente local.
   # Caso omitido, o sistema utilizará SQLite (sqlite:///local.db) automaticamente.
   ```
5. **Inicie a aplicação:**

   ```bash
   python app.py
   ```
6. **Acesse no navegador:**
   Abra [http://localhost:5000](http://localhost:5000)

---

## 🌐 Deploy em Produção (Render)

A aplicação está configurada para deploy simplificado na plataforma **Render**:

1. **Build Command:**

   ```bash
   pip install -r requirements.txt
   ```
2. **Start Command:**

   ```bash
   gunicorn app:app
   ```
3. **Variáveis de Ambiente Necessárias no Render:**

   - `SECRET_KEY`: Chave aleatória e segura para a sessão da aplicação.
   - `DATABASE_URL`: String de conexão fornecida pelo banco PostgreSQL gerenciado do Render (o `config.py` faz a conversão automática do protocolo `postgres://` para `postgresql+psycopg2://`).

---

## 👥 Contribuição

Contribuições são sempre bem-vindas!

1. Faça um Fork do projeto.
2. Crie uma Branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Faça o Commit de suas alterações (`git commit -m 'feat: adiciona nova funcionalidade'`).
4. Faça o Push para a Branch (`git push origin feature/nova-funcionalidade`).
5. Abra um **Pull Request**.

---

Desenvolvido para o **Projeto PEnsE** 🎓
