# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\migrations\0001_initial.py
# Compiled at: 2019-12-19 18:56:48
# Size of source mod 2**32: 10613 bytes
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion, markdownx.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='BaseInquiry',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))],
       options={'verbose_name':'問い合わせ関連', 
      'verbose_name_plural':'問い合わせ関連'}),
     migrations.CreateModel(name='Context',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'key', models.CharField(max_length=500, unique=True)),
      (
       'value', models.CharField(blank=True, max_length=500, null=True))]),
     migrations.CreateModel(name='ImageFile',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'file', models.ImageField(upload_to='images')),
      (
       'name', models.CharField(max_length=100))],
       options={'verbose_name':'写真', 
      'verbose_name_plural':'写真'}),
     migrations.CreateModel(name='Page',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=100)),
      (
       'in_nav', models.BooleanField(default=False)),
      (
       'path', models.CharField(blank=True, max_length=100, unique=True)),
      (
       'parent_page', models.ForeignKey(blank=True, help_text='パンくずリストの作成、SEO対策となります。', null=True, on_delete=(django.db.models.deletion.SET_NULL), to='django_press.Page', verbose_name='このページに親となるページ'))],
       options={'verbose_name':'Webページ', 
      'verbose_name_plural':'Webページ'}),
     migrations.CreateModel(name='PageContent',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'priority', models.PositiveSmallIntegerField(default=1, help_text='同じページ内では数値の重複を避けてください。\n0~32767の整数値で入力してください。\n小さい数字ほど上に来ます', verbose_name='ページ内の表示順(昇順)'))],
       options={'verbose_name':'ページの構成要素', 
      'verbose_name_plural':'ページの構成要素', 
      'ordering':('priority', )}),
     migrations.CreateModel(name='Product',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'icon', models.CharField(default='icofont icofont-light-bulb', help_text='https://icofont.com/icons 参照', max_length=100, verbose_name='icon class')),
      (
       'name', models.CharField(max_length=30, verbose_name='サービス名')),
      (
       'description', models.TextField(verbose_name='説明'))],
       options={'verbose_name':'紹介する系', 
      'verbose_name_plural':'紹介する系'}),
     migrations.CreateModel(name='TabElement',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=30, verbose_name='タブの見出し')),
      (
       'content', markdownx.models.MarkdownxField(help_text='Markdown、HTMLでの記述が可能です。ドラッグアンドドロップで画像の配置もできます。', verbose_name='タブの中身'))],
       options={'verbose_name':'タブ要素', 
      'verbose_name_plural':'タブ要素'}),
     migrations.CreateModel(name='Contact',
       fields=[
      (
       'baseinquiry_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='django_press.BaseInquiry')),
      (
       'category', models.CharField(choices=[('取引について', '取引について'), ('資料請求', '資料請求'), ('その他', 'その他')], max_length=10, verbose_name='お問い合わせカテゴリー')),
      (
       'name', models.CharField(max_length=20, verbose_name='お名前')),
      (
       'furigana', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='カタカナで入力してください。', regex='^[ｱ-ﾝア-ン\\s・]+$')], verbose_name='フリガナ')),
      (
       'email', models.EmailField(max_length=254)),
      (
       'phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='ハイフンなしで入力してください', regex='^[0-9]+$')], verbose_name='電話番号')),
      (
       'age', models.PositiveSmallIntegerField(verbose_name='年齢')),
      (
       'body', models.TextField(verbose_name='内容')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True))],
       options={'verbose_name':'問い合わせフォーム', 
      'verbose_name_plural':'問い合わせフォーム'},
       bases=('django_press.baseinquiry', )),
     migrations.CreateModel(name='ContactContent',
       fields=[
      (
       'pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='django_press.PageContent'))],
       options={'verbose_name': '問い合わせを使う'},
       bases=('django_press.pagecontent', )),
     migrations.CreateModel(name='ImageSlider',
       fields=[
      (
       'pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='django_press.PageContent')),
      (
       'content', models.ManyToManyField(to='django_press.ImageFile', verbose_name='画像'))],
       options={'verbose_name': '画像のスライドショー'},
       bases=('django_press.pagecontent', )),
     migrations.CreateModel(name='PageText',
       fields=[
      (
       'pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='django_press.PageContent')),
      (
       'content', markdownx.models.MarkdownxField(help_text='Markdown、HTMLでの記述が可能です。ドラッグアンドドロップで画像の配置もできます。', verbose_name='本文'))],
       options={'verbose_name': '文章と画像に最適'},
       bases=('django_press.pagecontent', )),
     migrations.CreateModel(name='Service',
       fields=[
      (
       'pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='django_press.PageContent')),
      (
       'title', models.CharField(max_length=30, verbose_name='見出し')),
      (
       'abstract', models.TextField(help_text='Markdown、HTMLでの記述が可能です。2,3行ぐらいが好ましいです。', verbose_name='概要')),
      (
       'products', models.ManyToManyField(to='django_press.Product', verbose_name='サービス'))],
       options={'verbose_name': 'サービスなどを伝える'},
       bases=('django_press.pagecontent', )),
     migrations.CreateModel(name='Tab',
       fields=[
      (
       'pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='django_press.PageContent')),
      (
       'tabs', models.ManyToManyField(to='django_press.TabElement', verbose_name='タブ要素'))],
       options={'verbose_name': 'タブを使う'},
       bases=('django_press.pagecontent', )),
     migrations.AddField(model_name='pagecontent',
       name='page',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='contents', to='django_press.Page')),
     migrations.AddField(model_name='pagecontent',
       name='polymorphic_ctype',
       field=models.ForeignKey(editable=False, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='polymorphic_django_press.pagecontent_set+', to='contenttypes.ContentType')),
     migrations.AddField(model_name='baseinquiry',
       name='polymorphic_ctype',
       field=models.ForeignKey(editable=False, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='polymorphic_django_press.baseinquiry_set+', to='contenttypes.ContentType')),
     migrations.AddField(model_name='contactcontent',
       name='form',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to='django_press.BaseInquiry', verbose_name='問い合わせ'))]