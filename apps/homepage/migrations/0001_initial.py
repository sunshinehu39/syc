# Generated by Django 2.0.4 on 2018-12-30 15:45

import DjangoUeditor.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, default='avatar/四叶草.png', max_length=200, null=True, upload_to='avatar', verbose_name='用户头像')),
                ('gender', models.CharField(choices=[('男', '男'), ('女', '女')], default='女', max_length=6, verbose_name='性 别')),
                ('is_vip', models.BooleanField(default=False, verbose_name='四叶草会员')),
                ('faved_list', models.TextField(blank=True, null=True, verbose_name='收藏列表')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='文章标题')),
                ('desc', models.CharField(max_length=50, verbose_name='文章描述')),
                ('content', DjangoUeditor.models.UEditorField(verbose_name='文章内容')),
                ('click_num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='推荐')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('top_index', models.IntegerField(default=0, verbose_name='置顶顺序')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('category', models.CharField(choices=[('阅读', '阅读'), ('思维导图', '思维导图'), ('写作', '写作'), ('演讲', '演讲'), ('其他', '其他')], default='其他', max_length=10, verbose_name='类 型')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作 者')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-date_publish'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('content', models.TextField(default='32个赞！', verbose_name='评论内容')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.Article', verbose_name='点评文章')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'ordering': ['-date_publish'],
            },
        ),
        migrations.CreateModel(
            name='GoldenWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copyright', models.CharField(choices=[('原创', '原创'), ('转载', '转载')], default='转载', max_length=4, verbose_name='版 权')),
                ('content', models.CharField(max_length=300, verbose_name='金句内容')),
                ('photo', models.ImageField(blank=True, default='photo/defult_goldwords.png', max_length=200, null=True, upload_to='photo', verbose_name='金句配图')),
                ('application', models.CharField(max_length=100, verbose_name='应用场景')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='推荐')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('top_index', models.IntegerField(default=0, verbose_name='置顶顺序')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('click_num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发布人')),
            ],
            options={
                'verbose_name': '金句',
                'verbose_name_plural': '金句',
                'ordering': ['-date_publish'],
            },
        ),
        migrations.CreateModel(
            name='GoodBooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='书籍名称')),
                ('author', models.CharField(blank=True, max_length=20, null=True, verbose_name='书籍作者')),
                ('bookcover', models.ImageField(blank=True, max_length=200, null=True, upload_to='bookcover', verbose_name='书籍封面')),
                ('bookreview', models.TextField(max_length=600, verbose_name='推荐词/书评')),
                ('url', models.URLField(blank=True, max_length=100, null=True, verbose_name='相关网址')),
                ('application', models.CharField(blank=True, max_length=100, null=True, verbose_name='适合人群')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('has_read', models.BooleanField(default=False, verbose_name='已读')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='推荐')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('top_index', models.IntegerField(default=0, verbose_name='置顶顺序')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('click_num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='推荐人')),
            ],
            options={
                'verbose_name': '好书',
                'verbose_name_plural': '好书',
                'ordering': ['-date_publish'],
            },
        ),
        migrations.CreateModel(
            name='GoodImgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodimg', models.ImageField(max_length=200, upload_to='goodimg', verbose_name='美图')),
                ('application', models.CharField(max_length=100, verbose_name='应用场景/图片主题')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='分享人')),
            ],
            options={
                'verbose_name': '美图',
                'verbose_name_plural': '美图',
                'ordering': ['-date_publish'],
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('description', models.CharField(max_length=200, verbose_name='友情链接描述')),
                ('callback_url', models.URLField(verbose_name='url地址')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('index', models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'ordering': ['index', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VipCard', models.ImageField(blank=True, max_length=200, null=True, upload_to='VipCard', verbose_name='四叶草会员卡')),
                ('syc_No', models.IntegerField(blank=True, null=True, unique=True, verbose_name='会员号')),
                ('role', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='角色')),
                ('join_time', models.DateField(blank=True, null=True, verbose_name='入会时间')),
                ('valid_time', models.DateField(blank=True, null=True, verbose_name='会员有效期')),
                ('study_num', models.IntegerField(default=0, verbose_name='参加活动数')),
                ('practise_num', models.IntegerField(default=0, verbose_name='风火轮打卡数')),
                ('url', models.URLField(blank=True, default='', max_length=100, null=True, verbose_name='个人网页地址')),
                ('video', models.URLField(blank=True, max_length=100, null=True, verbose_name='入会演讲视频地址')),
                ('profile', models.TextField(blank=True, default='', max_length=600, null=True, verbose_name='个人简介')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生年月')),
                ('wechat', models.CharField(blank=True, max_length=20, null=True, verbose_name='微信号')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号码')),
                ('join_team_time', models.DateField(blank=True, null=True, verbose_name='加入四叶草运营团队的时间')),
                ('click_num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('book_read', models.ManyToManyField(blank=True, to='homepage.GoodBooks', verbose_name='已读书籍')),
                ('name', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='姓名')),
            ],
            options={
                'verbose_name': '会员库',
                'verbose_name_plural': '会员库',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='标签名称')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_id', models.IntegerField(default=0, verbose_name='数据id')),
                ('fav_type', models.CharField(choices=[('文章', '文章'), ('好书', '好书'), ('美图', '美图'), ('金句', '金句'), ('会员', '会员')], default='文章', max_length=8, verbose_name='收藏类型')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Member', verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
            },
        ),
        migrations.AddField(
            model_name='goodimgs',
            name='tag',
            field=models.ManyToManyField(blank=True, to='homepage.Tag', verbose_name='标 签'),
        ),
        migrations.AddField(
            model_name='goodbooks',
            name='tag',
            field=models.ManyToManyField(blank=True, to='homepage.Tag', verbose_name='标 签'),
        ),
        migrations.AddField(
            model_name='goldenwords',
            name='tag',
            field=models.ManyToManyField(blank=True, to='homepage.Tag', verbose_name='标 签'),
        ),
        migrations.AddField(
            model_name='comment',
            name='goldwords',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.GoldenWords', verbose_name='点评金句'),
        ),
        migrations.AddField(
            model_name='comment',
            name='goodbooks',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.GoodBooks', verbose_name='点评好书'),
        ),
        migrations.AddField(
            model_name='comment',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.Member', verbose_name='点评会员'),
        ),
        migrations.AddField(
            model_name='comment',
            name='pid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.Comment', verbose_name='父级点评'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(blank=True, to='homepage.Tag', verbose_name='标 签'),
        ),
    ]
