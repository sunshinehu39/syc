
# 参考教程 https://www.cnblogs.com/wumingxiaoyao/p/6945769.html

import xadmin
from xadmin import views
from .models import *

class BaseSetting(object):
    # 显示主题
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "DOS圆梦大家庭管理后台"
    site_footer = "DOS运营团队"

    # show_bookmarks = false

    # 左侧菜单栏收缩功能
    # menu_style = "accordion"

    # global_search_models = [V_UserInfo,UserDistrict]
    #
    # global_models_icon = {
    #     V_UserInfo: "glyphicon glyphicon-user", UserDistrict: "fa fa-cloud"
    # }  # 设置models的全局图标

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

class ArticleAdmin(object):
    list_display = ["title","category","author", "click_num", "fav_num", "is_recommend", "is_top",
                    "top_index","date_publish", "tag"]
    search_fields = ['title', ]
    list_editable = ["is_recommend","is_top","top_index" ]
    list_filter = ["category","title","author", "click_num", "fav_num", "is_recommend", "is_top",
                    "top_index", "date_publish", "tag"]
    style_fields = {"content": "ueditor"}
    # show_detail_fields = ['top_index'] #显示数据详情
    # refresh_times = (3,5) #设置自动刷新时间，每3秒，每5秒

    # # 设置书签
    # list_bookmarks = [{
    # "title": "推荐",
    # "query": {"is_recommend": True},
    # "order": ("-click_num",),
    # "cols": ("title","category","author", "click_num"),
    # }]

class MemberAdmin(object):
    list_display = ["syc_No","name","role", "valid_time", "wechat",]
    search_fields = ["syc_No","name","role", "valid_time", ]
    list_editable = ["role" ]
    list_filter = ["valid_time"]

xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Tag)
xadmin.site.register(Links)
xadmin.site.register(GoldenWords)
xadmin.site.register(GoodBooks)
xadmin.site.register(GoodImgs)
xadmin.site.register(Comment)
xadmin.site.register(Member,MemberAdmin)