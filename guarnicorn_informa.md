#!/bin/bash

# Script de configuração do Gunicorn para um projeto Django
# Ajuste os valores conforme o seu ambiente e projeto.

# Variáveis do projeto
PROJECT_NAME="erp_mpro" # Nome do módulo principal (contém o wsgi.py)
PROJECT_DIR="/caminho/para/seu_projeto" # Diretório raiz do projeto
USER="seu_usuario" # Usuário que executará o serviço
GROUP="www-data" # Grupo para o serviço
VENV_DIR="$PROJECT_DIR/venv" # Caminho do ambiente virtual
GUNICORN_SOCKET="/run/gunicorn.sock" # Caminho do socket Gunicorn
WORKERS=3 # Número de workers Gunicorn

echo "===== Configuração do Gunicorn para o Projeto Django ====="

# 1. Certifique-se de que está no diretório do projeto
echo "1. Navegando para o diretório do projeto..."
cd "$PROJECT_DIR" || exit

# 2. Ativando o ambiente virtual
echo "2. Ativando o ambiente virtual..."
source "$VENV_DIR/bin/activate"

# 3. Instalando Gunicorn
echo "3. Instalando Gunicorn..."
pip install gunicorn

# 4. Testando o Gunicorn
echo "4. Testando o Gunicorn localmente..."
gunicorn "$PROJECT_NAME.wsgi:application" --bind 127.0.0.1:8000 --workers $WORKERS --timeout 120
echo "Teste concluído. Pressione Ctrl+C para parar o servidor após o teste."

# 5. Criando o serviço Systemd
echo "5. Configurando o serviço Systemd para o Gunicorn..."
SERVICE_FILE="/etc/systemd/system/gunicorn.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Gunicorn instance to serve Django project
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$PROJECT_DIR
ExecStart=$VENV_DIR/bin/gunicorn \
    --workers $WORKERS \
    --bind unix:$GUNICORN_SOCKET \
    $PROJECT_NAME.wsgi:application

[Install]
WantedBy=multi-user.target
EOL

# 6. Reiniciando o Systemd e iniciando o Gunicorn
echo "6. Iniciando e habilitando o serviço Gunicorn..."
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 7. Configurando o Nginx
echo "7. Configurando o Nginx..."
NGINX_CONF="/etc/nginx/sites-available/$PROJECT_NAME"

sudo bash -c "cat > $NGINX_CONF" <<EOL
server {
    listen 80;
    server_name exemplo.com www.exemplo.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $PROJECT_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$GUNICORN_SOCKET;
    }
}
EOL

# Criar o link simbólico para ativar a configuração
sudo ln -s $NGINX_CONF /etc/nginx/sites-enabled/

# Testar e reiniciar o Nginx
sudo nginx -t && sudo systemctl restart nginx

# Finalizando
echo "Configuração concluída! O Gunicorn está rodando e o Nginx está configurado."
echo "Certifique-se de atualizar 'server_name' no arquivo Nginx com o domínio ou IP correto."



Configuração do **Gunicorn** em um projeto Django:


# Configuração do Gunicorn no Projeto Django

## 1. Instalação do Gunicorn
Certifique-se de que o Gunicorn está instalado no ambiente virtual do projeto:

```bash
pip install gunicorn
```

---

## 2. Testando o Gunicorn Localmente
Execute o comando abaixo para testar o servidor Gunicorn:

```bash
gunicorn <nome_do_projeto>.wsgi:application
```

Substitua `<nome_do_projeto>` pelo diretório onde está localizado o arquivo `wsgi.py`. Por exemplo:

```bash
gunicorn erp_mpro.wsgi:application
```

Por padrão, o servidor será iniciado em `http://127.0.0.1:8000`.

---

## 3. Tornar o Servidor Acessível Externamente
Para acessar o servidor na rede, use:

```bash
gunicorn <nome_do_projeto>.wsgi:application --bind 0.0.0.0:8000
```

---

## 4. Configuração para Produção
Para um ambiente de produção, configure o Gunicorn com múltiplos workers:

```bash
gunicorn <nome_do_projeto>.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 120
```

### Parâmetros:
- `--workers`: Número de processos (recomendação: `2 * núcleos de CPU + 1`).
- `--threads`: Threads por processo.
- `--timeout`: Tempo limite para reiniciar um worker (em segundos).

---

## 5. Configuração de Serviço Systemd
Para gerenciar automaticamente o Gunicorn no Linux, crie um arquivo de serviço:

1. Crie o arquivo `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=Gunicorn instance to serve Django Project
After=network.target

[Service]
User=seu_usuario
Group=www-data
WorkingDirectory=/caminho/para/projeto
ExecStart=/caminho/para/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    <nome_do_projeto>.wsgi:application

[Install]
WantedBy=multi-user.target
```

2. Recarregue e inicie o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## 6. Configuração de Proxy Reverso com Nginx (Opcional)
Recomenda-se usar o Nginx para gerenciar conexões HTTP. Crie um arquivo de configuração:

1. Crie o arquivo `/etc/nginx/sites-available/django_project`:

```nginx
server {
    listen 80;
    server_name seu_dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /caminho/para/projeto;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

2. Ative a configuração:

```bash
sudo ln -s /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 7. Verificação e Logs
- Verifique se o Gunicorn está rodando:
  ```bash
  sudo systemctl status gunicorn
  ```
- Logs do Gunicorn:
  ```bash
  journalctl -u gunicorn
  ```
- Logs do Nginx:
  ```bash
  cat /var/log/nginx/error.log
  ```

---

## Observações
- Sempre teste o projeto localmente com o servidor de desenvolvimento antes de usar o Gunicorn:
  ```bash
  python manage.py runserver
  ```
- Garanta que os arquivos estáticos estejam configurados corretamente para produção.

---
``` 

Este documento pode ser adaptado para atender às necessidades específicas do seu projeto.