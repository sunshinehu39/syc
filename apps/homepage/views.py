from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings  # 引用全局变量
from django.db.models import Count,Q
from django.views.generic import ListView

from .models import *
from .forms import *

import datetime

#视图函数：全局变量
def global_setting(request):

    # 网站基本信息
    SITE_URL = settings.SITE_URL  # 网站地址
    SITE_NAME = settings.SITE_NAME  # 网站名称
    SITE_DESC = settings.SITE_DESC  # 网站描述
    SITE_COPYRIGHT = settings.SITE_COPYRIGHT  # 网站版权
    MEDIA_URL = settings.MEDIA_URL  # 上传文件的根目录

    # 浏览排行
    Most_viewed_list = Article.objects.all().order_by('-click_num')[:6]         #按点击率倒序（大到小），截取前6个

    #评论排行（先统计评论数目，后根据评论数目排行）
    comment_count_list = Comment.objects.values('article').exclude(article=None).annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]

    # 站长推荐
    Recommend_list = Article.objects.filter(is_recommend=True)[:6]

    # 标签
    tag_list = Tag.objects.all()[:8]

    # 文章归档
    archive_list = Article.objects.distinct_date()

    # 友情链接
    links_list = Links.objects.all()[:6]

    return locals()


# 视图函数-搜索
def searchView(request):
    search_keywords = request.GET.get("keywords", "")
    category = request.GET.get('category', None)

    if search_keywords:
        if category == 'None':
            article_list = Article.objects.filter(Q(title__contains=search_keywords)
                                                  | Q(desc__contains=search_keywords)
                                                  | Q(content__icontains=search_keywords)
                                                  | Q(author__username__contains=search_keywords)
                                                  | Q(tag__name__icontains=search_keywords)
                                                  | Q(category__icontains=search_keywords)
                                                  ).order_by("-date_publish").distinct()
            list_template = 'index.html'

        elif category == '好书':
            GoodBooks_list = GoodBooks.objects.filter(Q(name__contains=search_keywords)
                                                      | Q(author__contains=search_keywords)
                                                      | Q(bookreview__icontains=search_keywords)
                                                      | Q(application__icontains=search_keywords)
                                                      | Q(publisher__username__icontains=search_keywords)
                                                      | Q(tag__name__icontains=search_keywords)
                                                      ).order_by("-date_publish").distinct()
            list_template = 'GoodBooks.html'

        elif category == '美图':
            GoodImgs_list = GoodImgs.objects.filter(Q(application__contains=search_keywords)
                                                      | Q(publisher__username__icontains=search_keywords)
                                                      ).order_by("-date_publish").distinct()
            list_template = 'GoodImgs.html'

        elif category == '金句':

            # 评论表单
            form = GoldenWordsForm()

            GoldenWords_list = GoldenWords.objects.filter(Q(copyright__contains=search_keywords)
                                                      | Q(content__contains=search_keywords)
                                                      | Q(application__icontains=search_keywords)
                                                      | Q(publisher__username__icontains=search_keywords)
                                                      | Q(tag__name__icontains=search_keywords)
                                                      ).order_by("-date_publish").distinct()
            list_template = 'GoldenWords.html'

        elif category == '会员':
            Members_list = Member.objects.filter(
                                                Q(name__gender__contains=search_keywords)
                                               | Q(name__username__contains=search_keywords)
                                              # | Q(birthday__contains=search_keywords)
                                              # | Q(wechat__icontains=search_keywords)
                                              # | Q(mobile__icontains=search_keywords)
                                               | Q(syc_No__icontains=search_keywords)
                                               | Q(profile__icontains=search_keywords)
                                               # | Q(join_time__icontains=search_keywords)
                                               # | Q(valid_time__icontains=search_keywords)
                                               # | Q(is_valid__icontains=search_keywords)
                                              ).order_by("-join_time").distinct()
            list_template = 'Members.html'
        else:
            article_list = Article.objects.filter(category=category).filter(Q(title__contains=search_keywords)
                                                                            | Q(desc__contains=search_keywords)
                                                                            | Q(content__icontains=search_keywords)
                                                                            | Q(author__username__contains=search_keywords)
                                                                            | Q(tag__name__icontains=search_keywords)
                                                                            ).order_by("-date_publish").distinct()
            list_template = 'index.html'

    return render(request,list_template,locals())

# 通用类视图-首页-文章列表
class IndexView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'article_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 3


    def get_queryset(self):
        category = self.request.GET.get('category', None)

        if category == None:
            post_lists = Article.objects.all().order_by('-is_top', 'top_index', '-date_publish')
        elif category == 'None':
            post_lists = Article.objects.all().order_by('-is_top', 'top_index', '-date_publish')
        elif category == '四叶草':
            post_lists = []
        else:
            post_lists = Article.objects.filter(category=category).order_by('-is_top', 'top_index', '-date_publish')
        return post_lists

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 自定义额外传递的参数
        try:
            user_id = self.request.user.id
            member_id = Member.objects.get(name=user_id).id

            faved_goodbooks_list1 = UserFavorite.objects.filter(fav_type='文章')
            faved_goodbooks_list = faved_goodbooks_list1.filter(member_id=member_id).distinct()
            faved_list = []
            for faved_goodbook in faved_goodbooks_list:
                faved_list.append(faved_goodbook.fav_id)

            context.update({
                'category': self.request.GET.get('category', None),
                'faved_list': faved_list,
            })
        except:
            context.update({
                'category': self.request.GET.get('category', None),
            })

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# 通用类视图-金句列表
class GoldenWordsView(ListView):
    model = GoldenWords
    template_name = 'GoldenWords.html'
    context_object_name = 'GoldenWords_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 2

    def get_queryset(self):
        post_lists = GoldenWords.objects.all().order_by('-is_top', 'top_index', '-date_publish')
        return post_lists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #自定义额外传递的参数
        try:
            user_id = self.request.user.id
            member_id = Member.objects.get(name=user_id).id

            faved_goodbooks_list1 = UserFavorite.objects.filter(fav_type='金句')
            faved_goodbooks_list = faved_goodbooks_list1.filter(member_id=member_id).distinct()
            faved_list = []
            for faved_goodbook in faved_goodbooks_list:
                faved_list.append(faved_goodbook.fav_id)

            context.update({
                'category': self.request.GET.get('category', None),
                'form': GoldenWordsForm(),
                'faved_list':faved_list,
            })

        except:
            context.update({
                'category': self.request.GET.get('category', None),
                'form': GoldenWordsForm(),
            })

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# 视图函数-金句详情
def GoldenWords_detailView(request):
    try:
        category = request.GET.get('category', None)
        id = request.GET.get('id', None)
        goldenwords = GoldenWords.objects.get(pk=id)

        goldenwords.click_num += 1
        goldenwords.save()

        # 获取评论信息
        comments = Comment.objects.filter(goldwords=goldenwords)
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)

        return render(request, 'GoldenWords_detail.html', locals())
    except:
        return redirect('/')

#视图函数：添加金句
def add_GoldWordView(request):

    if request.method == 'POST':
        form = GoldenWordsForm(request.POST, request.FILES)
        form.save()

    redirect_to = '/GoldenWords?category=金句'

    return redirect(redirect_to)

# 通用类视图-好书列表
class GoodBooksView(ListView):
    model = GoodBooks
    template_name = 'GoodBooks.html'
    context_object_name = 'GoodBooks_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 2

    def get_queryset(self):
        post_lists = GoodBooks.objects.all().order_by('-is_top','top_index','-date_publish')
        return post_lists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #自定义额外传递的参数
        try:
            user_id = self.request.user.id
            member_id = Member.objects.get(name=user_id).id

            book_list = Member.objects.filter(pk=member_id).values_list('book_read')
            has_read_list = []
            for book in book_list:
                has_read_list.append(book[0])

            faved_goodbooks_list1 = UserFavorite.objects.filter(fav_type='好书')
            faved_goodbooks_list = faved_goodbooks_list1.filter(member_id=member_id).distinct()
            faved_list = []
            for faved_goodbook in faved_goodbooks_list:
                faved_list.append(faved_goodbook.fav_id)

            context.update({
                'category': self.request.GET.get('category', None),
                'faved_list':faved_list,
                'has_read_list':has_read_list,
            })

        except:
            context.update({
                'category': self.request.GET.get('category', None),
            })

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# 视图函数-好书详情
def GoodBook_detailView(request):

    try:
        category = request.GET.get('category', None)
        id = request.GET.get('id', None)
        goodbook = GoodBooks.objects.get(pk=id)

        goodbook.click_num += 1
        goodbook.save()

        # 获取评论信息
        comments = Comment.objects.filter(goodbooks=goodbook)
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)

        return render(request, 'GoodBooks_detail.html', locals())
    except:
        return redirect('/')

# 通用类视图-美图列表
class GoodImgsView(ListView):
    model = GoodImgs
    template_name = 'GoodImgs.html'
    context_object_name = 'GoodImgs_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 8

    def get_queryset(self):
        post_lists = GoodImgs.objects.all()
        return post_lists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 自定义额外传递的参数
        try:
            user_id = self.request.user.id
            member_id = Member.objects.get(name=user_id).id

            faved_goodbooks_list1 = UserFavorite.objects.filter(fav_type='美图')
            faved_goodbooks_list = faved_goodbooks_list1.filter(member_id=member_id).distinct()
            faved_list = []
            for faved_goodbook in faved_goodbooks_list:
                faved_list.append(faved_goodbook.fav_id)

            context.update({
                'category': self.request.GET.get('category', None),
                'faved_list': faved_list,
            })
        except:
            context.update({
                'category': self.request.GET.get('category', None),
            })

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# 通用类视图-会员列表
class MembersView(ListView):
    model = Member
    template_name = 'Members.html'
    context_object_name = 'Members_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 4

    def get_queryset(self):
        Members_list = Member.objects.all()

        rank = self.request.GET.get('rank', None)
        sex = self.request.GET.get('sex', None)
        comment_rank = self.request.GET.get('comment_rank', None)
        remind = self.request.GET.get('remind', None)

        if rank:
            Members_list = Member.objects.all().order_by(rank)

        if sex:
            Members_list = Member.objects.filter(name__gender=sex)

        if comment_rank:
            # 评论排行（先统计评论数目，后根据评论数目排行）
            comment_count_list = Comment.objects.values('member').exclude(member=None).annotate(
                comment_count=Count('member')).order_by(comment_rank)
            Members_list = [Member.objects.get(pk=comment['member']) for comment in comment_count_list]

        if remind:
            today = str(datetime.datetime.now())
            year = today[:4]
            month = today[5:7]
            datamark = year + '-' + month
            Members_list = Member.objects.filter(valid_time__icontains=datamark)

        return Members_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)



        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        category = '会员'
        rank = self.request.GET.get('rank', None)
        sex = self.request.GET.get('sex', None)
        comment_rank = self.request.GET.get('comment_rank', None)
        remind = self.request.GET.get('remind', None)

        context.update({
            'category':category,
        })

        if rank:
            path = '&rank='+rank
            context.update({
                'category': category,
                'rank': rank,
                'path':path
            })

        if sex:
            path = '&sex='+sex
            context.update({
                'category': category,
                'sex': sex,
                'path':path
            })

        if comment_rank:
            path = '&comment_rank='+comment_rank
            context.update({
                'category': category,
                'comment_rank': comment_rank,
                'path':path
            })

        if remind:
            path = '&remind='+remind
            context.update({
                'category': category,
                'remind': remind,
                'path':path
            })

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# 视图函数-会员详情
def Member_detailView(request):
    category = request.GET.get('category', None)
    id = request.GET.get('id', None)
    member = Member.objects.get(pk=id)

    member.click_num +=1
    member.save()

    # 获取评论信息
    comments = Comment.objects.filter(member=member).exclude(member=None)
    comment_list = []
    for comment in comments:
        for item in comment_list:
            if not hasattr(item, 'children_comment'):
                setattr(item, 'children_comment', [])
            if comment.pid == item:
                item.children_comment.append(comment)
                break
        if comment.pid is None:
            comment_list.append(comment)

    return render(request,'Member_detail.html',locals())



# 视图函数-添加收藏
def favView(request):
    category = request.GET.get('category', None)
    fav_type = category
    fav_id = request.GET.get('id', None)

    try:
        member_id = Member.objects.get(name=request.user.id).id

        has_faved = UserFavorite.objects.filter(fav_type=fav_type, fav_id=fav_id,member_id=member_id)

        if has_faved:
            has_faved.delete()
        else:
            fav = UserFavorite.objects.create(fav_type=fav_type,
                                             fav_id=fav_id,
                                             member_id=member_id,
                                             )
            fav.save()

        fav_num = UserFavorite.objects.filter(fav_type = category).filter(fav_id=fav_id).count()
        GoodBooks.objects.filter(id =fav_id ).update(fav_num=fav_num)

        if category == '文章':
            redirect_to = request.POST.get('next', request.GET.get('next', ''))
        else:
            redirect_to = request.POST.get('next', request.GET.get('next', '')) + '&category=' + category

        return redirect(redirect_to)
    except:
        return redirect('/')

# 视图函数-标记已读
def read_MarkView(request):
    category = request.GET.get('category', None)
    book_id = request.GET.get('id', None)
    user_id = request.user.id

    try:
        Member_id = Member.objects.get(name=user_id).id

        has_read = Member.objects.filter(pk = Member_id).filter(book_read__id__icontains = book_id)

        if has_read:
            Member.objects.get(pk = Member_id).book_read.remove(book_id)
        else:
            Member.objects.get(pk = Member_id).book_read.add(book_id)

        redirect_to = request.POST.get('next', request.GET.get('next', ''))+'&category='+category
        return redirect(redirect_to)
    except:
        return redirect('/')

# 视图函数-会员中心
def Member_centerView(request):

    if request.GET.get('show',):
        show=True

    user_id = request.user.id

    try:
        member_id = Member.objects.get(name_id=user_id).id
    except:
        return redirect('/')

    member = Member.objects.get(pk=member_id)
    user = User.objects.get(id=user_id)

    fav_type = request.GET.get('fav_type','')

    if fav_type == '好书':
        GoodBooks_list = UserFavorite.objects.filter(member_id=member_id,fav_type='好书').distinct()
        fav_list = []
        for GoodBook in GoodBooks_list:
            fav_list.append(GoodBook.id)

    if fav_type == '金句':
        GoldenWords_id_list = UserFavorite.objects.filter(member_id=member_id, fav_type='金句').distinct().values_list('fav_id')
        fav_list = []
        for GoldenWords_id in GoldenWords_id_list:
            fav_list.append(GoldenWords_id[0])

        GoldenWords_list = GoldenWords.objects.filter(id__in = fav_list)

    if fav_type == '文章':
        article_id_list = UserFavorite.objects.filter(member_id=member_id, fav_type='文章').distinct().values_list(
            'fav_id')
        fav_list = []
        for article_id in article_id_list:
            fav_list.append(article_id[0])

            article_list = Article.objects.filter(id__in=fav_list)

    if fav_type == '美图':
        article_id_list = UserFavorite.objects.filter(member_id=member_id, fav_type='美图').distinct().values_list(
            'fav_id')
        fav_list = []
        for article_id in article_id_list:
            fav_list.append(article_id[0])

            GoodImgs_list = GoodImgs.objects.filter(id__in=fav_list)

    if fav_type == '':
        fav_list = []

    fav_num = len(fav_list)

    return render(request,'Member_center.html',locals())

def update_memberView(request):
    user_id = request.user.id
    member_id = Member.objects.get(name_id=user_id).id

    user = User.objects.get(id=user_id)
    user.gender=request.POST.get('gender','男')
    user.email = request.POST.get('email','')
    user.save()

    import re

    # 正则匹配电话号码
    mobile = request.POST.get('mobile', '')
    p2 = re.compile('^(13[0-9]{9})|(15[89][0-9]{8})$')
    phonematch = p2.match(mobile)

    member = Member.objects.get(id=member_id)

    if phonematch:
        member.mobile = request.POST.get('mobile', '')
        error = ""
    else:
        error = "手机号码有误，请重新输入！   "

    member.role = request.POST.get('role', '')
    member.url = request.POST.get('url', '')
    member.birthday = request.POST.get('birthday', '')
    member.wechat = request.POST.get('wechat', '')
    member.profile = request.POST.get('profile', '')

    try:
        member.save()
    except:
        pass

    member = Member.objects.get(name_id=user_id)
    user = User.objects.get(id=user_id)

    show=True

    return render(request,'Member_center.html',locals())


# 裁剪头像
def img_cropView(request):
    return render(request,'img_crop.html',locals())

# 视图函数-上传裁剪后的头像
import base64,random,datetime
def img_postView(request):
    user_id = request.user.id
    member_id = Member.objects.get(name_id=user_id).id
    member = Member.objects.get(id=member_id)

    # 裁剪后的图片是base64编码数据，用base64.b64decode还原成图片后保存到数据库中
    strs = request.POST.get('photo', '').split(",")[1]
    imgdata = base64.b64decode(strs)

    # 将datetime转换为字符串的时间戳
    now = datetime.datetime.now()
    time_stamp = datetime.datetime.strftime(now, '%Y_%m_%d_%H_%M_%S_')

    imgname = time_stamp+str(random.randint(0,100))
    file = open('upload/avatar/'+imgname+'.jpg', 'wb')
    file.write(imgdata)
    file.close()
    avatar = 'avatar/'+imgname+'.jpg'

    if request.method == 'POST':
        User.objects.filter(id=user_id).update(avatar=avatar)

    member = Member.objects.get(name_id=user_id)
    user = User.objects.get(id=user_id)
    show=True
    redirect_to = '/Member_center?show=True'
    return redirect(redirect_to)
    # return render(request,'Member_center.html',locals())


#视图函数：文章详情、评论列表、评论表单
def article(request):

    category = request.GET.get('category', None)

    # 获取文章id
    id = request.GET.get('id', None)

    # 获取文章信息
    article = Article.objects.get(pk=id)

    # 每天成功打开一次，增加一个浏览量
    article.click_num +=1
    article.save()

    try:
        user_id = request.user.id
        member_id = Member.objects.get(name=user_id).id

        faved_goodbooks_list1 = UserFavorite.objects.filter(fav_type='文章')
        faved_goodbooks_list = faved_goodbooks_list1.filter(member_id=member_id).distinct()
        faved_list = []
        for faved_goodbook in faved_goodbooks_list:
            faved_list.append(faved_goodbook.fav_id)

    except:
        pass

    # 获取评论信息
    comments = Comment.objects.filter(article=article).exclude(article=None)
    comment_list = []
    for comment in comments:
        for item in comment_list:
            if not hasattr(item, 'children_comment'):
                setattr(item, 'children_comment', [])
            if comment.pid == item:
                item.children_comment.append(comment)
                break
        if comment.pid is None:
            comment_list.append(comment)

    return render(request, 'article.html', locals())

#视图函数：文章归档
def archive(request):
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    archive_article_list = Article.objects.filter(date_publish__icontains=year+'-'+month).order_by('-is_top','top_index','-date_publish')
    return render(request, 'archive.html', locals())

#视图函数：标签归档
def tag(request):
    category = request.GET.get('category', None)
    tid = request.GET.get('tid', None)
    tag = Tag.objects.get(pk=tid)

    if category == 'None':
        article_list = Article.objects.filter(tag=tag).order_by("-date_publish").distinct()
        list_template = 'index.html'

    elif category == '好书':
        GoodBooks_list = GoodBooks.objects.filter(tag=tag).order_by("-date_publish").distinct()
        list_template = 'GoodBooks.html'

    elif category == '美图':
        GoodImgs_list = GoodImgs.objects.filter(tag=tag).order_by("-date_publish").distinct()
        list_template = 'GoodImgs.html'

    elif category == '金句':

        # 评论表单
        form = GoldenWordsForm()

        GoldenWords_list = GoldenWords.objects.filter(tag=tag).order_by("-date_publish").distinct()
        list_template = 'GoldenWords.html'

    elif category == '会员':
        Members_list = Member.objects.filter(tag=tag).order_by("-join_time").distinct()
        list_template = 'Members.html'
    else:
        article_list = Article.objects.filter(category=category).filter(tag=tag).distinct()
        list_template = 'index.html'

    return render(request,list_template,locals())

#视图函数：发布评论
def comment_post(request):
    user_id = request.user.id
    content = request.POST.get('content', '32个赞！')

    if content == '<p><br></p>':
        content = '32个赞！'

    category = request.GET.get('category', 'None')

    if category == '会员':
        member_id = request.POST.get('id', None)

        comment = Comment.objects.create(user_id=user_id,
                                         content=content,
                                         member_id=member_id,
                                         )
        comment.save()

    elif category == '好书':
        goodbooks_id = request.POST.get('id', None)

        comment = Comment.objects.create(user_id=user_id,
                                         content=content,
                                         goodbooks_id=goodbooks_id,
                                         )
        comment.save()

    elif category == '金句':
        goldwords_id = request.POST.get('id', None)

        comment = Comment.objects.create(user_id=user_id,
                                         content=content,
                                         goldwords_id=goldwords_id,
                                         )
        comment.save()

    else:
        article_id = request.POST.get('id', None)

        comment = Comment.objects.create( user_id = user_id,
                                          content = content,
                                          article_id = article_id,
                                         )
        comment.save()

    redirect_to = request.POST.get('next', request.GET.get('next', ''))+'&category='+category
    return redirect(redirect_to)

#视图函数：注册
def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'registration/register.html', context={'form': form, 'next': redirect_to})

#视图函数：发邮件
def sendemail(request):
    from_email = settings.EMAIL_HOST_USER   # 获取发件人邮箱
    emailaddress = request.POST['email']   # 获取收件人邮箱

    if User.objects.filter(email=emailaddress):
        for i in User.objects.filter(email=emailaddress):
            nametemp = i.username
            idtemp = i.id

            # 生成随机密码
            from random import choice
            import string
            # python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters
            def GenPassword(length=8, chars=string.ascii_letters + string.digits):
                return ''.join([choice(chars) for i in range(length)])
            pawdtemp = GenPassword(8)

            User.objects.filter(email=emailaddress).delete()
            User.objects.create_user(id=idtemp, username=nametemp, password=pawdtemp,email=emailaddress)

            # 发送邮件
            from django.core.mail import send_mail
            send_mail(
                subject=u"这是新的密码,请使用新的密码登录",     # 邮件标题
                message=pawdtemp,                                 # 邮件内容
                from_email= from_email ,                          # 发件人邮箱
                recipient_list=[emailaddress, ],                  # 收件人邮箱
                fail_silently=False,
            )
            # return HttpResponse("新的密码已经发到您的邮箱,请去您的邮箱查收并使用新的密码登录,有问题请联系站长")
            return render(request, 'registration/password_reset_done.html')
    else:
        return HttpResponse("您的邮箱的账户注册信息没有找到")