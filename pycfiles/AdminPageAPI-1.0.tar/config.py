# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/adminish/config.py
# Compiled at: 2010-03-01 07:25:00
import pkg_resources, logging, couchish
log = logging.getLogger(__name__)

def make_adminish_config(couchish_config, store_factory=None, widget_registry_factory=None):
    """
    Build a configuration dict for adminish.

    :param: couchish_config the couchish config instance
    :param: store_factory func with signature store_factory(request) that will
            return the couchish store for the current request.
    :param: widget_registry_factory optional callable with signature f(store)
            that returns the widget registry used to construct editing forms.
    """
    config = {'store_factory': store_factory, 'widget_registry_factory': widget_registry_factory, 
       'types': {}}
    for (type, data) in couchish_config.types.items():
        metadata = dict(data.get('metadata', {}))
        labels = metadata.setdefault('labels', {})
        if 'singular' not in labels:
            labels['singular'] = type.title()
        if 'plural' not in labels:
            labels['plural'] = type.title() + 's'
        metadata.setdefault('pager', 'Paging')
        templates = metadata.setdefault('templates', {})
        if 'item' not in templates:
            templates['item'] = '/adminish/item.html'
        if 'new_item' not in templates:
            templates['new_item'] = '/adminish/new_item.html'
        if 'items' not in templates:
            templates['items'] = '/adminish/items.html'
        items_table = templates.get('items-table', [])
        for (n, entry) in enumerate(items_table):
            if 'label' in entry:
                items_table[n]['label'] = entry['label']
            else:
                items_table[n]['label'] = entry['name'].title()
            if 'value' in entry:
                items_table[n]['value'] = entry['value']

        config['types'][type] = metadata
        indexes = metadata.setdefault('indexes', [])
        for index in indexes:
            if 'label' not in index:
                index['label'] = index['name']
            if 'var' not in index:
                index['var'] = index['name']
            if 'data' not in index:
                index['data'] = '%%(%s)s' % index['var']
            if isinstance(index['data'], basestring):
                index['data'] = [
                 index['data']]
            if 'sortable' not in index:
                index['sortable'] = False
            if 'type' not in index:
                index['type'] = 'full'

    return config


def add_initial_data(couchish_config, store):
    """
    Build a configuration dict for adminish.

    :param: couchish_config the couchish config instance
    :param: store a couchish store
    """
    for (type, data) in couchish_config.types.items():
        initial_data = data.get('initial_data', [])
        for data in initial_data:
            data['model_type'] = type
            with store.session() as (S):
                S.create(data)


def make_couchish_config(app_conf, model_resource):
    (module, dir) = model_resource.split('.', 1)
    models = {}
    for f in pkg_resources.resource_listdir(module, dir):
        if f.endswith('.model.yaml'):
            (name, remaining) = f.split('.', 1)
            models[name] = pkg_resources.resource_filename(model_resource, f)

    views_file = pkg_resources.resource_filename(model_resource, 'views.yaml')
    return couchish.Config.from_yaml(models, views_file)