# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/checkbox.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3549 bytes
__doc__ = 'PyAMS_form.browser.checkbox module\n\nCheckbox widget implementation.\n'
from zope.interface import implementer_only
from zope.schema.interfaces import IBool, ITitledTokenizedTerm
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_form.browser.widget import HTMLInputWidget, add_field_class
from pyams_form.interfaces.widget import ICheckBoxWidget, IFieldWidget, ISingleCheckBoxWidget
from pyams_form.term import Terms
from pyams_form.util import to_unicode
from pyams_form.widget import FieldWidget, SequenceWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'

@implementer_only(ICheckBoxWidget)
class CheckBoxWidget(HTMLInputWidget, SequenceWidget):
    """CheckBoxWidget"""
    klass = 'checkbox-widget'
    css = 'checkbox'

    def is_checked(self, term):
        """Check if given term is selected"""
        return term.token in self.value

    @property
    def items(self):
        """Items list getter"""
        if self.terms is None:
            return ()
        items = []
        for count, term in enumerate(self.terms):
            checked = self.is_checked(term)
            item_id = '%s-%i' % (self.id, count)
            if ITitledTokenizedTerm.providedBy(term):
                label = self.request.localizer.translate(term.title)
            else:
                label = to_unicode(term.value)
            items.append({'id': item_id, 
             'name': self.name + ':list', 
             'value': term.token, 
             'label': label, 
             'checked': checked})

        return items

    def update(self):
        """See pyams_form.interfaces.widget.IWidget."""
        super(CheckBoxWidget, self).update()
        add_field_class(self)

    def json_data(self):
        """Get widget data in JSON format"""
        data = super(CheckBoxWidget, self).json_data()
        data['type'] = 'check'
        data['options'] = list(self.items)
        return data


def CheckBoxFieldWidget(field, request):
    """IFieldWidget factory for CheckBoxWidget."""
    return FieldWidget(field, CheckBoxWidget(request))


@implementer_only(ISingleCheckBoxWidget)
class SingleCheckBoxWidget(CheckBoxWidget):
    """SingleCheckBoxWidget"""
    klass = 'single-checkbox-widget'

    def update_terms(self):
        """Update terms"""
        if self.terms is None:
            self.terms = Terms()
            self.terms.terms = SimpleVocabulary((
             SimpleTerm('selected', 'selected', self.label or self.field.title),))
        return self.terms


@adapter_config(context=(IBool, IFormLayer), provides=IFieldWidget)
def SingleCheckBoxFieldWidget(field, request):
    """IFieldWidget factory for CheckBoxWidget."""
    widget = FieldWidget(field, SingleCheckBoxWidget(request))
    widget.label = ''
    return widget