from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'psycopg2',
    'jupyter',
    'networkx',
    'geoalchemy2'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    'tox'
]

setup(name='GerryPy',
      version='0.0',
      description='GerryPy',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author=['Jordan Schatzman',
              'Julian Wilson',
              'Patrick Saunders',
              'Avery Pratt',
              'Ford Fowler'],
      author_email=['jordan.schatzman@outlook.com',
                    'apratt91@gmail.com',
                    'julienawilson@gmail.com',
                    'fordjfowler@gmail.com'],
      url='http://gerrypy.herokuapp.com/',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = gerrypy:main
      [console_scripts]
      initialize_db = gerrypy.scripts.initializedb:main
      """,
      )
