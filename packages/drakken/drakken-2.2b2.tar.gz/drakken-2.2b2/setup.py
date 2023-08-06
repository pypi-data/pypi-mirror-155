from setuptools import setup

with open('README', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='drakken',
      version='2.2b2',
      description='Python web framework',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Craig Howard',
      author_email='craig@seagrape.us',
      install_requires=[
          'mako',
          'parse',
          'requests',
          'requests-wsgi-adapter',
          'sqlalchemy',
          'webob',
      ],
      keywords='Minimalist Python web framework',
      url='https://seagrape.us/drakken.html',
      packages=['drakken'],
      license='MIT',
      )

