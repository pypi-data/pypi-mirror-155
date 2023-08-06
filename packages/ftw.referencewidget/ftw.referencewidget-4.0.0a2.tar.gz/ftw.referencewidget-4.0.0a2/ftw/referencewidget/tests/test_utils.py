from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.interfaces import IReferenceSettings
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from ftw.referencewidget.tests.views.form import TestView
from ftw.referencewidget.utils import get_types_not_searched
from ftw.referencewidget.utils import set_types_not_searched
from plone.registry.interfaces import IRegistry
from unittest import TestCase
from zope.component import getUtility


class TestFieldConverter(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        self.widget = form.form_instance.widgets['relation']
        tns = get_types_not_searched(self.portal)
        tns = tns + ('Folder',)
        set_types_not_searched(self.portal, tns)

    def test_traversable_types_default(self):
        expected = ['Document', 'Event', 'File', 'Folder', 'Image',
                    'Link', 'News Item', 'Topic', 'Collection']
        result = get_traversal_types(self.widget)
        for item in result:
            self.assertIn(item, expected)

    def test_traversable_types_more_blocked(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IReferenceSettings)
        proxy.block_traversal_additional = ('Document', 'Link')

        result = get_traversal_types(self.widget)
        self.assertTrue('Document' not in result)
        self.assertTrue('Link' not in result)

    def test_traversable_types_more_allowed(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IReferenceSettings)
        proxy.traverse_additional = ('Folder',)

        result = get_traversal_types(self.widget)
        self.assertIn('Folder', result)

    def test_selectable_types_more_allowed(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IReferenceSettings)
        proxy.select_additional = ('Folder',)

        result = get_selectable_types(self.widget)
        self.assertIn('Folder', result)

    def test_selectable_types_more_blocked(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IReferenceSettings)
        proxy.block_additional = ('Document', 'Link')

        result = get_selectable_types(self.widget)
        self.assertNotIn('Document', result)
        self.assertNotIn('Link', result)
