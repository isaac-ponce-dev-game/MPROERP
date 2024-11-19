import os
import subprocess

# Configurações básicas
PROJECT_NAME = "MPROERP"
DOMAIN_NAME = "erp.nformasmoveis.com.br"
APP_DIR = "/home/isaac_ponce/MPROERP"
VENV_DIR = f"{APP_DIR}/venv"
SOCKET_FILE = f"{APP_DIR}/gunicorn.sock"
GUNICORN_SERVICE = "gunicorn.service"
NGINX_CONFIG_FILE = f"/etc/nginx/sites-available/{PROJECT_NAME}"
CLOUDFLARE_TUNNEL_CONFIG = "/etc/cloudflared/config.yml"

GITHUB_USER = "isaac-ponce-dev-game"
GITHUB_PASSWORD = "Poeta.2021"
GITHUB_REPO_NAME = "MPROERP"

def run_command(command):
    """Executa comandos shell."""
    try:
        print(f"Executando: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar: {command}\n{e}")
        raise

def remove_existing_configs():
    """Remove configurações antigas."""
    print("Removendo configurações existentes...")
    if os.path.exists(NGINX_CONFIG_FILE):
        run_command(f"sudo rm -f {NGINX_CONFIG_FILE}")
    run_command(f"sudo rm -f /etc/nginx/sites-enabled/{PROJECT_NAME}")
    
    # Remove links simbólicos quebrados
    for file in os.listdir("/etc/nginx/sites-enabled/"):
        filepath = f"/etc/nginx/sites-enabled/{file}"
        if not os.path.exists(filepath):  # Verifica se o arquivo alvo existe
            print(f"Removendo link simbólico inválido: {filepath}")
            run_command(f"sudo rm -f {filepath}")
    
    # Verifica se o serviço Gunicorn existe antes de desativar e remover
    try:
        run_command(f"sudo systemctl stop {GUNICORN_SERVICE}")
        run_command(f"sudo systemctl disable {GUNICORN_SERVICE}")
    except subprocess.CalledProcessError:
        print(f"Serviço {GUNICORN_SERVICE} não encontrado ou já desativado.")
    
    if os.path.exists(f"/etc/systemd/system/{GUNICORN_SERVICE}"):
        run_command(f"sudo rm -f /etc/systemd/system/{GUNICORN_SERVICE}")
    
    if os.path.exists(CLOUDFLARE_TUNNEL_CONFIG):
        run_command(f"sudo rm -f {CLOUDFLARE_TUNNEL_CONFIG}")
    
    run_command("sudo systemctl stop nginx")
    run_command("sudo systemctl stop cloudflared")
    run_command("sudo systemctl daemon-reload")



def create_nginx_config():
    """Cria configuração Nginx."""
    print("Criando configuração Nginx...")
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
    """Cria serviço Gunicorn."""
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
    run_command(f"sudo systemctl daemon-reload")
    run_command(f"sudo systemctl enable {GUNICORN_SERVICE}")

def create_cloudflare_tunnel():
    """Cria configuração do túnel Cloudflare."""
    print("Criando túnel do Cloudflare...")
    tunnel_config = f"""
tunnel: 2033a43b-6f55-4ed6-86b3-6255fa4f9798
credentials-file: /home/isaac_ponce/.cloudflared/2033a43b-6f55-4ed6-86b3-6255fa4f9798.json

ingress:
  - hostname: {DOMAIN_NAME}
    service: http://127.0.0.1:80
  - service: http_status:404
"""
    with open(f"/tmp/cloudflared.yml", "w") as f:
        f.write(tunnel_config)
    run_command(f"sudo mv /tmp/cloudflared.yml {CLOUDFLARE_TUNNEL_CONFIG}")
    run_command(f"sudo systemctl restart cloudflared")

def restart_services():
    """Reinicia os serviços."""
    print("Reiniciando serviços...")
    run_command("sudo systemctl restart nginx")
    run_command("sudo systemctl restart gunicorn")
    run_command("sudo systemctl restart cloudflared")

def setup_github_repo():
    """Configura repositório no GitHub."""
    print("Configurando repositório no GitHub...")
    run_command(f"curl -u {GITHUB_USER}:{GITHUB_PASSWORD} https://api.github.com/user/repos -d '{{\"name\":\"{GITHUB_REPO_NAME}\"}}'")
    run_command(f"cd {APP_DIR} && git init")
    run_command(f"cd {APP_DIR} && git remote add origin https://github.com/{GITHUB_USER}/{GITHUB_REPO_NAME}.git")
    run_command(f"cd {APP_DIR} && git add .")
    run_command(f"cd {APP_DIR} && git commit -m 'Initial commit'")
    run_command(f"cd {APP_DIR} && git push -u origin master")

if __name__ == "__main__":
    try:
        remove_existing_configs()
        create_nginx_config()
        create_gunicorn_service()
        create_cloudflare_tunnel()
        restart_services()
        setup_github_repo()
        print("Configuração concluída com sucesso!")
    except Exception as e:
        print(f"Erro durante a configuração: {e}")
