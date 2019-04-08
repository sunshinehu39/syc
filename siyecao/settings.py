
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,"apps"))
sys.path.insert(0,os.path.join(BASE_DIR,"extra_apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r2=m29x-(fl*!v%&_jcj6wxp@*-5o++hcofen5^w37)fw!**9b'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
# 部署上线时，关闭调试，设置为False
# DEBUG = False

# 允许外网访问
ALLOWED_HOSTS = ['*']

# Application definition

# 注册APP
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'homepage',
    'xadmin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'siyecao.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # 配置前端模板templates路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'homepage.views.global_setting',  # 将全局变量应用于所有模板，homepage为app名称
            ],
        },
    },
]

WSGI_APPLICATION = 'siyecao.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

#配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "siyecao", #数据库名称
        'USER': "root",
        'PASSWORD': "root",
        "HOST": "",  # 远程填ip,本地可不填
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 把英文改为中文
LANGUAGE_CODE = 'zh-hans'

# 把国际时区改为中国时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 关闭utc时间，系统将使用本地时间
USE_TZ = False

# 配置静态文件static路径
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# 设置文件上传路径
MEDIA_URL='/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/')

#这个是在浏览器上访问该上传文件的url的前缀

# 自定义全局变量，变量名需全部大写，不能出现小写字母

# 网站的基本信息配置
SITE_URL = 'http://127.0.0.1:8000/'
SITE_NAME = '四叶草学习社群'
SITE_DESC = '越学习，越幸运！'
SITE_COPYRIGHT = '读画写讲，疯狂成长！'

# model表中自定义用户表
AUTH_USER_MODEL = 'homepage.User'

LOGOUT_REDIRECT_URL = '/'   #注销后回到首页（next无访问路径时）
LOGIN_REDIRECT_URL = '/'    #登陆后进入首页（next无访问路径时）

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#163邮箱配置，需在邮箱设置中开启POP3/SMTP/IMAP服务，并自定义授权码
EMAIL_HOST= 'smtp.163.com'
EMAIL_PORT= 465
EMAIL_HOST_USER = "isyc666@163.com"
EMAIL_HOST_PASSWORD = "isyc666" # 自定义授权码
EMAIL_USE_SSL = True

# qq邮箱配置，需在邮箱设置中开启POP3/SMTP/IMAP服务，并生成第三方授权码
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'dos2012@qq.com' # 你的 QQ 邮箱账号
EMAIL_HOST_PASSWORD = 'aqplfnmipqlsbaee' # 邮箱账户设置里生成的第三方授权码
EMAIL_USE_TLS = True

