from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.referencewidget.tests import builders
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class FtwReferenceWidgetLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="plone.autoinclude" file="meta.zcml" />'
            '  <autoIncludePlugins target="plone" />'
            '  <autoIncludePluginsOverrides target="plone" />'
            '</configure>',
            context=configurationContext)

        import ftw.referencewidget.tests.views
        xmlconfig.file('configure.zcml',
                       ftw.referencewidget.tests.views,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.referencewidget:default')
        applyProfile(portal, 'collective.z3cform.datagridfield:default')
        applyProfile(portal, 'plone.app.contenttypes:default')

        file_fti = portal.portal_types.File
        file_behaviors = list(file_fti.behaviors)
        file_behaviors.remove('plone.namefromfilename')
        file_behaviors += ['plone.app.content.interfaces.INameFromTitle']
        file_fti.behaviors = tuple(file_behaviors)


FTW_REFERENCE_FIXTURE = FtwReferenceWidgetLayer()


FTW_REFERENCE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_REFERENCE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.referencewidget:functional")
