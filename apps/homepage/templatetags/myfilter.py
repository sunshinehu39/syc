# -*- coding: utf-8 -*-
from django import template
register = template.Library()
from homepage.models import User,Member,GoodBooks

# 自定义过滤器：小数转换为百分数显示
@register.filter
def percent(value):
    return str(int(value*100)) + '%'

@register.filter
def bookcover(value):
    bookcover = GoodBooks.objects.get(pk=value).bookcover
    return bookcover

# 自定义过滤器：将<br/>替换为\r\n，以便在textarea显示换行！
@register.filter
def tshow(value):
    return value.replace("<br/>", '\r\n').strip()

@register.filter
def has_read(value,request):
    user_id = request.user.id
    Member_id = Member.objects.get(name=user_id).id
    has_read = Member.objects.filter(pk = Member_id).filter(book_read__id__icontains = value)

    if has_read:
        return "已读"
    else:
        return "标记为已读！"

@register.filter
def M_id(value):
    id = Member.objects.get(name_id=value).id
    return id

# 自定义过滤器：将日期中的月份转换为大写的过滤器，如8转换为八
@register.filter
def month_to_upper(key):
        return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][key.month-1]

# 自定义过滤器：在文章详情页，标记"站长推荐"
@register.filter
def recommend(value):
        if value :
                return "强烈推荐！"
        else:
                return ""

# 自定义过滤器：根据用户性别选择头像
@register.filter
def photo(value):
        if value == '男':
                return "static/images/user_boy.jpg"
        elif value == '女':
                return "static/images/user_girl.jpg"
        else:
                return "static/images/user_x.jpg"

@register.filter
def sex(value):
    if value == '男':
        return "#09F"
    elif value == '女':
        return "crimson"

@register.filter
def sextag(value):
    if value == '男':
        return "#09F"
    elif value == '女':
        return "crimson"

@register.filter
def Chat_bubble(value):
    if value == '男':
        return "Chat_bubble_male"
    elif value == '女':
        return "Chat_bubble_female"

@register.filter
def is_top (value):
    if value :
        return "置顶"
    else:
        return ""



# 自定义的过滤器，若字符串长度大于15，则省略之后的内容，否则原样输出该字符串。参数value就是过滤器前的值
@register.filter(name='truncate_filter')
def truncate_chars(value):
    if len(value) > 40 :
        return '%s ……'% value[0:40]
    else:
        return value