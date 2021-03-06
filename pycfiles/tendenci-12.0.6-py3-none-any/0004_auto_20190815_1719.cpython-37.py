# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/pages/migrations/0004_auto_20190815_1719.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1555 bytes
from django.db import migrations

def remove_google_profile_from_page_view(apps, schema_editor):
    """
    Remove the google_profile block from pages/view.html
    
        {% if page.google_profile %}
          {% if page.has_google_author %}
          <a href="{{ page.google_profile }}?rel=author">{% trans "View Author's Google+ Profile" %}</a>
          {% elif page.has_google_publisher %}
          <a href="{{ page.google_profile }}" rel="publisher">{% trans "View Publisher's Google+ Page" %}</a>
          {% endif %}
        {% endif %}
    
    """
    import re, os
    from tendenci.apps.theme.utils import get_theme_root
    dir_path = get_theme_root()
    file_path = '{}/templates/pages/view.html'.format(dir_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as (f):
            content = f.read()
            p = '{0}([\\d\\D\\s\\S\\w\\W]*?){1}([\\s\\S]*?){2}'.format(re.escape('{% if page.google_profile %}'), re.escape('{% endif %}'), re.escape('{% endif %}'))
            content = re.sub(p, '', content)
        with open(file_path, 'w') as (f):
            f.write(content)


class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0003_remove_page_google_profile')]
    operations = [
     migrations.RunPython(remove_google_profile_from_page_view)]