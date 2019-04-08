
from django.db import models
from django.contrib.auth.models import AbstractUser

from DjangoUeditor.models import UEditorField

# 数据表建模：标签Tag
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 数据表建模：用户User
# 采用的继承方式扩展用户信息（本系统采用），扩展：关联的方式去扩展用户信息
class User(AbstractUser):
    avatar = models.ImageField(verbose_name='用户头像', default='avatar/四叶草.png', upload_to='avatar', max_length=200,
                               blank=True, null=True)
    gender=models.CharField(verbose_name='性 别',default='女',max_length=6,choices=(("男", u"男"), ("女", u"女")))
    is_vip = models.BooleanField(verbose_name='四叶草会员', default=False)
    faved_list = models.TextField(verbose_name='收藏列表',blank=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

# 数据表建模：美图
class GoodImgs(models.Model):
    goodimg = models.ImageField(verbose_name='美图',upload_to='goodimg',max_length=200)
    application = models.CharField(verbose_name='应用场景/图片主题', max_length=100)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='分享人')
    date_publish = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    tag = models.ManyToManyField(Tag, verbose_name='标 签', blank=True)

    class Meta:
        verbose_name = '美图'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.application


# 自定义管理器：文章ArticleManager
# 1、新加一个数据处理的方法
# 2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            year = date['date_publish'].strftime('%Y')
            month = date['date_publish'].strftime('%m')
            date = year + '年' + month + '月 文章归档'
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


# 数据表建模：文章Article
class Article(models.Model):
    title = models.CharField(verbose_name='文章标题', max_length=30)
    desc = models.CharField(verbose_name='文章描述', max_length=50)
    content = UEditorField(verbose_name="文章内容", imagePath="Article/images/", filePath="Article/files/", width=700,
                           height=300)
    click_num = models.IntegerField(verbose_name='浏览量', default=0)
    fav_num = models.IntegerField(verbose_name="收藏数", default=0)
    is_recommend = models.BooleanField(verbose_name='推荐', default=False)
    is_top = models.BooleanField(verbose_name='置顶', default=False)
    top_index = models.IntegerField(verbose_name="置顶顺序", default=0)
    date_publish = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作 者')

    CATEGORY_CHOICES = (
        ('阅读', '阅读'),
        ('思维导图', '思维导图'),
        ('写作', '写作'),
        ('演讲', '演讲'),
        ('其他', '其他'),
    )

    category = models.CharField(verbose_name='类 型', default='其他', max_length=10, choices=CATEGORY_CHOICES)

    tag = models.ManyToManyField(Tag, verbose_name='标 签', blank=True)

    objects = ArticleManager()  # 引入自定义管理器：文章ArticleManager

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

# 数据表建模：友情链接Links
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title

# 数据表建模：好书
class GoodBooks(models.Model):
    name = models.CharField(verbose_name='书籍名称', max_length=20)
    author = models.CharField(verbose_name='书籍作者', max_length=20, blank=True, null=True)
    bookcover = models.ImageField(verbose_name='书籍封面', upload_to='bookcover',
                              max_length=200, blank=True, null=True)
    bookreview = models.TextField(verbose_name='推荐词/书评',max_length=600)
    url = models.URLField(verbose_name='相关网址',max_length=100, blank=True, null=True)
    application = models.CharField(verbose_name='适合人群', max_length=100, blank=True, null=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='推荐人')
    tag = models.ManyToManyField(Tag, verbose_name='标 签', blank=True)
    fav_num = models.IntegerField(verbose_name="收藏数", default=0)

    has_read = models.BooleanField(verbose_name='已读', default=False)
    is_recommend = models.BooleanField(verbose_name='推荐', default=False)
    is_top = models.BooleanField(verbose_name='置顶', default=False)
    top_index = models.IntegerField(verbose_name="置顶顺序", default=0)
    date_publish = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    click_num = models.IntegerField(verbose_name='浏览量', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '好书'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']


# 数据表建模：金句 GoldenWords
class GoldenWords(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发布人')
    copyright = models.CharField(verbose_name='版 权', default='转载', max_length=4, choices=(("原创", "原创"), ("转载", "转载")))
    content = models.CharField(verbose_name='金句内容', max_length=300)
    photo = models.ImageField(verbose_name='金句配图',default='photo/defult_goldwords.png', upload_to='photo',
                               max_length=200, blank=True, null=True)
    application = models.CharField(verbose_name='应用场景', max_length=100)
    tag = models.ManyToManyField(Tag, verbose_name='标 签',blank=True)
    click_num = models.IntegerField(verbose_name='浏览量', default=0)
    fav_num = models.IntegerField(verbose_name="收藏数", default=0)
    is_recommend = models.BooleanField(verbose_name='推荐', default=False)
    is_top = models.BooleanField(verbose_name='置顶', default=False)
    top_index = models.IntegerField(verbose_name="置顶顺序", default=0)
    date_publish = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    click_num = models.IntegerField(verbose_name='浏览量', default=0)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '金句'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

# 数据表建模：标签Tag
class Member(models.Model):
    VipCard = models.ImageField(verbose_name='四叶草会员卡',upload_to='VipCard',max_length=200,null=True, blank=True)
    syc_No = models.IntegerField(verbose_name="会员号",unique=True,blank=True, null=True)
    name = models.OneToOneField(User, verbose_name='姓名',blank=True, null=True, on_delete=models.CASCADE)
    role = models.CharField(verbose_name='角色',default='',max_length=100,blank=True, null=True)
    join_time = models.DateField(verbose_name="入会时间",null=True, blank=True)
    valid_time = models.DateField(verbose_name="会员有效期",null=True, blank=True)
    study_num = models.IntegerField(verbose_name='参加活动数', default=0)
    practise_num = models.IntegerField(verbose_name='风火轮打卡数', default=0)
    url = models.URLField(verbose_name='个人网页地址',max_length=100,default='', blank=True, null=True)
    video = models.URLField(verbose_name='入会演讲视频地址',max_length=100, blank=True, null=True)
    profile = models.TextField(verbose_name='个人简介', max_length=600,default='',blank=True, null=True)

    birthday = models.DateField(verbose_name="出生年月",null=True, blank=True)
    wechat = models.CharField(verbose_name='微信号',max_length=20, blank=True, null=True)
    mobile = models.CharField(verbose_name='手机号码',max_length=11,unique=True,blank=True, null=True)
    join_team_time = models.DateField(verbose_name="加入四叶草运营团队的时间",null=True, blank=True)
    click_num = models.IntegerField(verbose_name='浏览量', default=0)
    book_read = models.ManyToManyField(GoodBooks, verbose_name='已读书籍', blank=True)

    class Meta:
        verbose_name = '会员库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name.username


# 数据表建模：评论Comment
class Comment(models.Model):
    pid = models.ForeignKey('self',verbose_name='父级点评', blank=True,null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户',blank=True, null=True, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(verbose_name='发布时间',auto_now_add=True )
    content = models.TextField(verbose_name='评论内容',default="32个赞！")
    article = models.ForeignKey(Article,verbose_name='点评文章', blank=True, null=True, on_delete=models.CASCADE)
    goldwords = models.ForeignKey(GoldenWords, verbose_name='点评金句', blank=True, null=True,on_delete=models.CASCADE)
    goodbooks = models.ForeignKey(GoodBooks,verbose_name='点评好书', blank=True,null=True, on_delete=models.CASCADE)
    member = models.ForeignKey(Member,verbose_name='点评会员', blank=True,null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.content

class UserFavorite(models.Model):
    member = models.ForeignKey(Member,verbose_name=u"用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0,verbose_name=u"数据id")
    fav_type = models.CharField(verbose_name=u"收藏类型",choices=(("文章","文章"),("好书","好书"),("美图","美图"),("金句","金句"),("会员","会员")),default="文章",max_length=8)
    add_time = models.DateTimeField(verbose_name=u"添加时间",auto_now_add=True)

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name