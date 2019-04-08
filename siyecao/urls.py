from django.urls import path, re_path,include  # 导入django自带的url路径函数,path为绝对匹配，re_path为正则匹配

# 配置xadmin
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

from apps.homepage.views import *

# 路径索引对应视图函数
urlpatterns = [
    path('xadmin', xadmin.site.urls),
    re_path(r'^ueditor/', include('DjangoUeditor.urls')),
    path('syc', IndexView.as_view(), name='syc'),

    # ^  不能省！
    re_path('^', include('homepage.urls')),

    # 将 auth 应用中的 urls 模块包含进来
    re_path(r'^users/', include('django.contrib.auth.urls')),
]

from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
