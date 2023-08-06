from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISearchSchema
from zope.component import getUtility


def get_types_not_searched(context):

    return api.portal.get_registry_record('plone.types_not_searched')


def set_types_not_searched(context, types):
    registry = getUtility(IRegistry)
    search_settings = registry.forInterface(ISearchSchema, prefix='plone')
    search_settings.types_not_searched = tuple(types)
