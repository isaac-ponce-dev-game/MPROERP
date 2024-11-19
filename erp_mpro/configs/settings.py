import os
from decouple import config, Csv
from dj_database_url import parse as dburl
from .configs import (
    DEFAULT_DATABASE_URL,
    DEFAULT_FROM_EMAIL,
    EMAIL_HOST,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_PORT,
    EMAIL_USE_TLS
)

# Caminhos do projeto
APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(APP_ROOT))

# Configurações de segurança
SECRET_KEY = config('SECRET_KEY')  # Mantenha a chave secreta fora do código-fonte
DEBUG = config('DEBUG', default=False, cast=bool)  # Desative o DEBUG em produção
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())  # Defina os hosts permitidos
ALLOWED_HOSTS = ['erp.nformasmoveis.com.br', '127.0.0.1', 'localhost']

# Configuração do banco de dados
if not DEFAULT_DATABASE_URL:
    DEFAULT_DATABASE_URL = f'sqlite:///{os.path.join(APP_ROOT, "db.sqlite3")}'

DATABASES = {
    'default': config('DATABASE_URL', default=DEFAULT_DATABASE_URL, cast=dburl),
}

# Aplicativos instalados
INSTALLED_APPS = [
    # Apps nativos do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    # Apps do projeto erp_mpro
    'erp_mpro.apps.base',
    'erp_mpro.apps.login',
    'erp_mpro.apps.cadastro',
    'erp_mpro.apps.vendas',
    'erp_mpro.apps.compras',
    'erp_mpro.apps.fiscal',
    'erp_mpro.apps.financeiro',
    'erp_mpro.apps.estoque',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware personalizado para login obrigatório
    'erp_mpro.middleware.LoginRequiredMiddleware',
]

# Configuração das URLs e templates
ROOT_URLCONF = 'erp_mpro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Processadores de contexto personalizados
                'erp_mpro.apps.base.context_version.sige_version',
                'erp_mpro.apps.login.context_user.foto_usuario',
            ],
        },
    },
]

WSGI_APPLICATION = 'erp_mpro.wsgi.application'

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configurações de localização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configurações de arquivos estáticos e mídia
STATIC_URL = '/static/'
STATIC_ROOT = '/home/isaac_ponce/MPROERP/staticfiles'
STATICFILES_DIRS = [os.path.join(APP_ROOT, 'static')]
FIXTURE_DIRS = [os.path.join(APP_ROOT, 'fixtures')]

MEDIA_ROOT = os.path.join(APP_ROOT, 'media/')
MEDIA_URL = '/media/'

# Configurações de sessão
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# URLs que não exigem login
LOGIN_NOT_REQUIRED = (
    r'^/login/$',
    r'/login/esqueceu/',
    r'/login/trocarsenha/',
    r'/logout/',
)
