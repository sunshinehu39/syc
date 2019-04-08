# APP专用url配置
from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page  # view缓存优化，导入cache_page 装饰器

urlpatterns = [
    path('Member_center', Member_centerView, name='Member_center'),  # 会员中心
    path('img_crop', img_cropView, name='img_crop'),                         # 头像裁剪
    path('img_post', img_postView, name='img_post'),                         # 头像提交
    path('update_member', update_memberView, name='update_member'),         # 更新会员资料

    path('fav', favView, name='fav'),                                    # 收藏
    path('read_Mark', read_MarkView, name='read_Mark'),                 # 标记已读

    path('tag', tag, name='tag'),                                   # 标签
    path('archive',archive, name='archive'),                       # 文章归档

    path('article', article, name='article'),                     # 文章详情

    path('comment/post/', comment_post, name='comment_post'),    # 提交评论
    path('add_GoldWord', add_GoldWordView, name='add_GoldWord'),  # 添加金句

    path('register', register, name='register'),                  # 注册
    path('sendemail', sendemail, name='sendemail'),  # 将新密码发送到邮箱

    path('GoldenWords',GoldenWordsView.as_view(), name='GoldenWords'),  # 金句库-列表
    path('GoldenWords_detail', GoldenWords_detailView, name='GoldenWords_detail'),  # 金句-详情
    path('GoodBooks', GoodBooksView.as_view(), name='GoodBooks'),       # 好书-列表
    path('GoodBook_detail', GoodBook_detailView, name='GoodBook_detail'),  # 好书-详情

    path('GoodImgs', GoodImgsView.as_view(), name='GoodImgs'),          # 美图-列表
    path('Members', MembersView.as_view(), name='Members'),             #会员-列表
    path('Member_detail', Member_detailView, name='Member_detail'),    #会员详情
]
