🚀 Launcher de Programas

Launcher de aplicativos e jogos para Windows desenvolvido em Python usando PySide6.
O objetivo do projeto é fornecer uma interface simples para organizar, abrir e monitorar o tempo de uso de programas e jogos instalados no computador.

O launcher funciona como uma pequena biblioteca de aplicativos, permitindo gerenciar executáveis (.exe) em um único lugar.

📸 Interface

Principais elementos da interface:

campo de busca para encontrar rapidamente programas

lista com ícones dos executáveis

contador de tempo de uso

tema claro / escuro

personalização de cores

✨ Funcionalidades
🔎 Busca de Programas

Permite localizar rapidamente aplicativos digitando parte do nome.

Exemplo:

chr

resultado:

chrome.exe
➕ Adicionar Executáveis

Permite adicionar qualquer .exe ao launcher.

Ao adicionar:

o caminho do programa é salvo

o ícone do executável é extraído automaticamente

o aplicativo passa a aparecer na lista

▶️ Executar Programas

O launcher inicia programas usando o método equivalente ao duplo clique do Windows, garantindo compatibilidade com jogos e aplicativos.

O sistema define automaticamente:

diretório de execução

caminho correto do executável

⏱️ Monitoramento de Tempo de Uso

O launcher registra quanto tempo cada programa ficou aberto.

Exemplo:

Chrome — 2h 14m
GTAIV.exe — 5h 33m

Essas informações são salvas em:

usage.json
🧹 Remover Programas

Executáveis podem ser removidos da lista a qualquer momento.

O launcher remove apenas o registro interno, não desinstala o programa do computador.

🎨 Tema Personalizável

O usuário pode escolher uma cor para o tema da interface.

Essa cor será aplicada aos elementos da UI:

botões

campos de texto

destaques visuais

🌙 Dark Mode

O launcher possui modo escuro integrado com alternância instantânea.

Configuração salva automaticamente em:

settings.json
🖼️ Ícones Automáticos

Ao adicionar um programa, o launcher:

extrai o ícone do .exe

salva em:

icons/

utiliza esse ícone na lista de aplicativos.

Isso garante carregamento rápido da interface.

🏗️ Estrutura do Projeto
LauncherDeProgramas
│
├── launcher.py
├── apps.json
├── usage.json
├── settings.json
├── icons/
└── README.md
launcher.py

Arquivo principal contendo toda a lógica da aplicação.

apps.json

Armazena os executáveis adicionados.

Exemplo:

[
  {
    "name": "chrome.exe",
    "path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "icon": "icons/chrome.exe.ico"
  }
]
usage.json

Armazena o tempo de uso acumulado.

Exemplo:

{
  "chrome.exe": 5420,
  "gtaiv.exe": 13240
}

Valores são armazenados em segundos.

settings.json

Configurações do launcher.

{
 "dark_mode": true,
 "theme_color": "#3daee9"
}
icons/

Contém os ícones extraídos automaticamente dos executáveis.

🛠️ Tecnologias Utilizadas

Python

PySide6

psutil

JSON para persistência de dados

Git para versionamento

⚙️ Instalação
1️⃣ Clonar o repositório
git clone https://github.com/lfaz3245/LanucherDeProgramas.git
2️⃣ Entrar na pasta
cd LanucherDeProgramas
3️⃣ Instalar dependências
pip install PySide6 psutil
4️⃣ Executar o programa
python launcher.py
📦 Gerar Executável

Para criar um executável Windows utilize PyInstaller.

Instale:

pip install pyinstaller

Gerar executável:

pyinstaller --onefile --noconsole launcher.py

O executável será criado em:

dist/launcher.exe
📌 Roadmap

Melhorias planejadas para futuras versões:

biblioteca visual de jogos estilo Steam

capas de jogos

estatísticas semanais de uso

suporte a categorias

minimizar para system tray

detecção automática de jogos instalados

exportar dados de uso

📄 Licença

Este projeto é distribuído sob a licença MIT.

👨‍💻 Autor

Projeto desenvolvido por:

Elifaz Emanuel

GitHub
https://github.com/lfaz3245
