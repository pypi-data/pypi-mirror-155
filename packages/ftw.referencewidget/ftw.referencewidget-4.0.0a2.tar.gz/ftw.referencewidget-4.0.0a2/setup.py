from setuptools import setup, find_packages
import os

version = '4.0.0a2'
maintainer = 'Mathias Leimgruber'

tests_require = [
    'collective.z3cform.datagridfield',
    'plone.app.testing',
    'ftw.builder',
    'ftw.testing',
    'ftw.testbrowser'
]

setup(name='ftw.referencewidget',
      version=version,
      description="A reference browser widget (Maintainer %s)" % maintainer,

      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),

      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Plone',
          'Framework :: Plone :: 6.0',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9',
      ],

      keywords='ftw 4teamwork widget reference browser',
      author='%s, 4teamwork AG' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.referencewidget',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'Plone',
          'collective.z3cform.datagridfield',
          'setuptools',
          'plone.app.registry',
          'z3c.relationfield',
          'plone.z3cform',
          'plone.app.z3cform',
          'plone.app.intid',
          'plone.app.relationfield',
          'ftw.upgrade',
          'plone.api',
          'plone.restapi',
      ],

      extras_require=dict(
          tests=tests_require,
          test=tests_require,
      ),
      tests_require=tests_require,

      entry_points="""
      # -*- Entry points: -*-
      [plone.autoinclude.plugin]
      target = plone
      """,
      )
