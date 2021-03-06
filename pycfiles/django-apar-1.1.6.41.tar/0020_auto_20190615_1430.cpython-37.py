# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0020_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 5987 bytes
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0019_auto_20190526_1043')]
    operations = [
     migrations.AlterModelOptions(name='basecourse',
       options={'verbose_name':'دوره پایه', 
      'verbose_name_plural':'دوره های پایه'}),
     migrations.AlterModelOptions(name='course',
       options={'verbose_name':'دوره', 
      'verbose_name_plural':'دوره ها'}),
     migrations.AlterModelOptions(name='coursefile',
       options={'verbose_name':'فایل', 
      'verbose_name_plural':'فایل ها'}),
     migrations.AlterModelOptions(name='coursesegment',
       options={'verbose_name':'بخش دوره', 
      'verbose_name_plural':'بخش دوره ها'}),
     migrations.AlterModelOptions(name='coursesummary',
       options={'ordering':('id', ), 
      'verbose_name':'خلاصه دوره',  'verbose_name_plural':'خلاصه دوره'}),
     migrations.AlterField(model_name='basecourse',
       name='description',
       field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='توضیحات')),
     migrations.AlterField(model_name='course',
       name='banner',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='course_banner', to='filefields.FileField', verbose_name='بنر')),
     migrations.AlterField(model_name='course',
       name='category_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='categories.Category', verbose_name='دسته بندی')),
     migrations.AlterField(model_name='course',
       name='cover',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='course_cover', to='filefields.FileField', verbose_name='تصویر جلد')),
     migrations.AlterField(model_name='course',
       name='dependency_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='dependency', to='courses.Course', verbose_name='وابستگی')),
     migrations.AlterField(model_name='course',
       name='parent_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='courses.Course', verbose_name='والد')),
     migrations.AlterField(model_name='course',
       name='publish_date',
       field=models.DateTimeField(default=(django.utils.timezone.now), verbose_name='تاریخ انتشار')),
     migrations.AlterField(model_name='course',
       name='publish_day',
       field=models.CharField(blank=True, choices=[('1', 'شنبه'), ('2', 'یکشنبه'), ('3', 'دوشنبه'), ('4', 'سه شنبه'), ('5', 'چهارشنبه'), ('6', 'پنج شنبه'), ('7', 'جمعه')], max_length=1, null=True, verbose_name='روز')),
     migrations.AlterField(model_name='course',
       name='publish_month',
       field=models.CharField(blank=True, choices=[('1', 'فروردین'), ('2', 'اردیبهشت'), ('3', 'خرداد'), ('4', 'تیر'), ('5', 'مرداد'), ('6', 'شهریور'), ('7', 'مهر'), ('8', 'آبان'), ('9', 'آذر'), ('10', 'دی'), ('11', 'بهمن'), ('12', 'اسفند')], max_length=2, null=True, verbose_name='ماه')),
     migrations.AlterField(model_name='course',
       name='publish_week',
       field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True, verbose_name='هفته')),
     migrations.AlterField(model_name='course',
       name='teacher_obj',
       field=models.ManyToManyField(blank=True, to='teachers.Teacher', verbose_name='مدرسین')),
     migrations.AlterField(model_name='coursefile',
       name='course_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='courses.Course', verbose_name='دوره')),
     migrations.AlterField(model_name='coursefile',
       name='seconds',
       field=models.BigIntegerField(default=0, verbose_name='زمان')),
     migrations.AlterField(model_name='coursesummary',
       name='course',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='total_times', to='courses.BaseCourse', verbose_name='دوره')),
     migrations.AlterField(model_name='coursesummary',
       name='file_count',
       field=models.PositiveIntegerField(default=0, verbose_name='تعداد فایل ها')),
     migrations.AlterField(model_name='coursesummary',
       name='file_count_preview',
       field=models.PositiveIntegerField(default=0, verbose_name='تعداد فایل های پیش نمایش')),
     migrations.AlterField(model_name='coursesummary',
       name='total_time_seconds',
       field=models.BigIntegerField(default=0, verbose_name='زمان')),
     migrations.AlterField(model_name='coursesummary',
       name='type',
       field=models.CharField(choices=[('M', 'فیلم'), ('V', 'صدا'), ('P', 'پی دی اف'), ('I', 'عکس')], max_length=1, verbose_name='نوع'))]