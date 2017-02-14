# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.settings
#
# Configuración de funcionalidades y parámetros del sistema
# @author Generated by 'django-admin startproject' using Django 1.7.
# @author Jorge Redondo (jredondo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
import os


## Directorio base desde donde se encuentra ejecutando la aplicación
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^_uj&#+hs!=q57!%!ao%t#e$^q@8qtxh$3ejf@uh4rnw#igqwu'

## Identifica si el sistema se encuentra en modo de desarrollo (True) o en modo producción (False)
DEBUG = True

## Identifica a los servidores permitidos que atienden las peticiones del sistema
ALLOWED_HOSTS = ['*']


## Listado de aplicaciones base del sistema
PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
]

if DEBUG:
    ## Aplicaciones requeridas para entornos de desarrollo
    PREREQ_APPS += [
        'django_extensions',
        'debug_toolbar',
    ]

    ## Configuracion de parametros de django-debug-toolbar
    JQUERY_URL = ''

## Listado de aplicaciones del projecto
PROJECT_APPS = [
    'topic_explorer',
]

## Listado de aplicaciones cargadas por el sistema
INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE_CLASSES += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

## Configuración de las URL del sistema
ROOT_URLCONF = 'django_topic_explorer.urls'

## Ruta de los templates
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

## Ruta de los archivos del pre-procesamiento
PROCESAMIENTO_PATH = os.path.join(BASE_DIR, 'files')


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_PATH,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                "django.template.context_processors.tz",
            ],
        },
    },
]

## Configuración para el wsgi de la aplicación
WSGI_APPLICATION = 'django_topic_explorer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

## Configuración del código del lenguaje a utilizar por defecto
LANGUAGE_CODE = 'es-ve'

## Configuración para el nombre de localización por defecto
LOCALE_NAME = 'es'

## Configuración para la zona horaria por defecto
TIME_ZONE = 'America/Caracas'

## Determina si se emplea la internacionalización I18N
USE_I18N = True

## Determina si se emplea la internacionalización L10N
USE_L10N = True

## Determina si se emplea la zona horaria
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

## Configuración de la raíz donde se encuentran los archivos estaticos del sistema (para entornos en producción)
STATIC_ROOT = ''

## Configuración de la url que atenderá las peticiones de los archivos estáticos del sistema
STATIC_URL = '/static/'

## Configuración de los directorios en donde se encuentran los archivos estáticos
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

## URL de acceso al sistema
#LOGIN_URL = "/login"

## URL de salida del sistema
#LOGOUT_URL = "/logout"

## configuración que permite obtener la ruta en donde se encuentran las traducciones de la aplicación a otros lenguajes
LOCALE_PATHS = [
    #os.path.join(BASE_DIR, 'locale'),
]

## Registro de mensajes al usuario
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

## TOPIC EXPLORER SETTINGS
TOPIC_EXPLORER_PATH = '/home/rodrigo/Proyectos/Interpretacion/'
FILES_PATH = TOPIC_EXPLORER_PATH +'demo-data/prueba/noaccent'
#FILES_PATH = TOPIC_EXPLORER_PATH +'demo-data/ap/'
#CORPUS_FILE = MODELS_PATH + 'pp-nltk-en-freq5.npz'
#CORPUS_FILE = MODELS_PATH + 'corpus.npz'
LDA_DATA_PATH = TOPIC_EXPLORER_PATH + 'demo-data/prueba/lda/algo{0}/'
LDA_CORPUS_FILE = TOPIC_EXPLORER_PATH + 'demo-data/prueba/lda_corpus/corpus.dat'
LDA_VOCAB_FILE = TOPIC_EXPLORER_PATH + 'demo-data/prueba/lda_corpus/vocab.txt'
LDA_CORPUS_DIR = TOPIC_EXPLORER_PATH +'demo-data/prueba/pp'

#MODEL_PATTERN = MODELS_PATH + 'pp-nltk-en-freq5-LDA-K{0}-document-200.npz'
#MODEL_PATTERN = MODELS_PATH + 'ap-nltk-en-freq5-LDA-K{0}-document-20.npz'
CONTEXT_TYPE = 'document'
#TOPICS = '10, 20, 30, 40, 50, 60, 70'
#TOPICS = '10, 20, 30, 40, 50, 60, 70, 80, 90, 100'
#TOPICS = '15, 30, 40, 50, 60, 70, 80, 90'
TOPICS = '10, 20, 30, 40, 50, 60, 70, 80, 90'
CORPUS_NAME = 'Deafult'

CORPUS_LINK = None
TOPIC_RANGE = None
DOC_TITTLE_FORMAT = None
DOC_URL_FORMAT = None
