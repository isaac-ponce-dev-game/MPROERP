import os
import subprocess
import requests

# Configurações básicas
PROJECT_NAME = "MPROERP"
DOMAIN_NAME = "erp.nformasmoveis.com.br"
APP_DIR = "/home/isaac_ponce/MPROERP"
VENV_DIR = f"{APP_DIR}/venv"
SOCKET_FILE = f"{APP_DIR}/gunicorn.sock"
GUNICORN_SERVICE = "gunicorn.service"
NGINX_CONFIG_FILE = f"/etc/nginx/sites-available/{PROJECT_NAME}"
CLOUDFLARE_TUNNEL_CONFIG = "/etc/cloudflared/config.yml"
GITHUB_USERNAME = "isaac-ponce-dev-game"
REPO_NAME = "MPROERP"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Defina o token como variável de ambiente
GITHUB_API_URL = "https://api.github.com"

if not GITHUB_TOKEN:
    raise EnvironmentError("Variável de ambiente 'GITHUB_TOKEN' não está definida. Configure antes de continuar.")

def run_command(command):
    """Executa comandos shell."""
    try:
        print(f"Executando: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {command}\n{e}")
        raise

def remove_existing_configs():
    """Remove configurações antigas de Nginx, Gunicorn e Cloudflare."""
    print("Removendo configurações existentes...")
    # Nginx
    run_command(f"sudo rm -f {NGINX_CONFIG_FILE}")
    run_command(f"sudo rm -f /etc/nginx/sites-enabled/{PROJECT_NAME}")

    # Remover links simbólicos inválidos
    for link in os.listdir("/etc/nginx/sites-enabled/"):
        link_path = f"/etc/nginx/sites-enabled/{link}"
        if not os.path.exists(link_path):
            print(f"Removendo link simbólico inválido: {link_path}")
            run_command(f"sudo rm -f {link_path}")

    # Gunicorn
    run_command(f"sudo systemctl stop {GUNICORN_SERVICE} || true")
    run_command(f"sudo systemctl disable {GUNICORN_SERVICE} || true")
    run_command(f"sudo rm -f /etc/systemd/system/{GUNICORN_SERVICE}")

    # Cloudflare Tunnel
    run_command(f"sudo rm -f {CLOUDFLARE_TUNNEL_CONFIG}")

    # Reload Nginx e systemd
    run_command("sudo systemctl stop nginx || true")
    run_command("sudo systemctl stop cloudflared || true")
    run_command("sudo systemctl daemon-reload")

def create_nginx_config():
    """Cria uma configuração para o Nginx."""
    print("Criando configuração do Nginx...")
    config = f"""
server {{
    listen 80;
    server_name {DOMAIN_NAME};

    location /static/ {{
        alias {APP_DIR}/staticfiles/;
    }}

    location /media/ {{
        alias {APP_DIR}/media/;
    }}

    location / {{
        proxy_pass http://unix:{SOCKET_FILE};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
    with open(f"/tmp/{PROJECT_NAME}", "w") as f:
        f.write(config)
    run_command(f"sudo mv /tmp/{PROJECT_NAME} {NGINX_CONFIG_FILE}")
    run_command(f"sudo ln -s {NGINX_CONFIG_FILE} /etc/nginx/sites-enabled/")

def create_gunicorn_service():
    """Cria um arquivo de configuração de serviço para o Gunicorn."""
    print("Criando serviço Gunicorn...")
    service = f"""
[Unit]
Description=gunicorn daemon for {PROJECT_NAME}
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory={APP_DIR}
ExecStart={VENV_DIR}/bin/gunicorn --workers 3 --bind unix:{SOCKET_FILE} erp_mpro.wsgi:application

[Install]
WantedBy=multi-user.target
"""
    with open(f"/tmp/{GUNICORN_SERVICE}", "w") as f:
        f.write(service)
    run_command(f"sudo mv /tmp/{GUNICORN_SERVICE} /etc/systemd/system/")
    run_command("sudo systemctl daemon-reload")
    run_command("sudo systemctl enable gunicorn.service")

def create_cloudflare_tunnel():
    """Cria uma configuração para o túnel Cloudflare."""
    print("Criando túnel Cloudflare...")
    config = f"""
tunnel: 2033a43b-6f55-4ed6-86b3-6255fa4f9798
credentials-file: /home/isaac_ponce/.cloudflared/2033a43b-6f55-4ed6-86b3-6255fa4f9798.json

ingress:
  - hostname: {DOMAIN_NAME}
    service: http://127.0.0.1:80
  - service: http_status:404
"""
    with open(f"/tmp/cloudflared.yml", "w") as f:
        f.write(config)
    run_command(f"sudo mv /tmp/cloudflared.yml {CLOUDFLARE_TUNNEL_CONFIG}")
    run_command("sudo systemctl restart cloudflared")

def restart_services():
    """Reinicia os serviços Nginx, Gunicorn e Cloudflare."""
    print("Reiniciando serviços...")
    run_command("sudo systemctl restart nginx")
    run_command("sudo systemctl restart gunicorn")
    run_command("sudo systemctl restart cloudflared")

def create_github_repo(repo_name, description=""):
    """Cria ou verifica se um repositório existe no GitHub."""
    print(f"Verificando se o repositório '{repo_name}' já existe no GitHub...")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    
    # Verifica se o repositório já existe
    response = requests.get(f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}", headers=headers)
    if response.status_code == 200:
        print(f"Repositório '{repo_name}' já existe. Continuando...")
        return

    if response.status_code == 404:
        print(f"Repositório '{repo_name}' não encontrado. Criando...")
        payload = {
            "name": repo_name,
            "description": description,
            "private": False,
        }
        response = requests.post(f"{GITHUB_API_URL}/user/repos", headers=headers, json=payload)
        if response.status_code == 201:
            print(f"Repositório '{repo_name}' criado com sucesso!")
        else:
            print(f"Erro ao criar repositório no GitHub: {response.json()}")
            response.raise_for_status()
    else:
        print(f"Erro ao verificar repositório no GitHub: {response.json()}")
        response.raise_for_status()

def configure_git():
    """Inicializa o repositório Git e faz o push inicial."""
    print("Configurando Git...")
    run_command(f"cd {APP_DIR} && git init")
    
    # Verifica se o remoto já existe
    try:
        run_command(f"cd {APP_DIR} && git remote add origin https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
    except subprocess.CalledProcessError:
        print("Remoto 'origin' já existe. Atualizando URL do remoto.")
        run_command(f"cd {APP_DIR} && git remote set-url origin https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
    
    run_command(f"cd {APP_DIR} && git add .")
    run_command(f'cd {APP_DIR} && git commit -m "Initial commit"')
    run_command(f"cd {APP_DIR} && git push -u origin master")


if __name__ == "__main__":
    try:
        remove_existing_configs()
        create_nginx_config()
        create_gunicorn_service()
        create_cloudflare_tunnel()
        restart_services()
        create_github_repo(REPO_NAME)
        configure_git()
        print("Configuração concluída com sucesso!")
    except Exception as e:
        print(f"Erro durante a configuração: {e}")
