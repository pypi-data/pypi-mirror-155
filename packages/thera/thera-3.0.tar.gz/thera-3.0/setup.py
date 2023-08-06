from setuptools import setup

with open('README', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='thera',
      version='3.0',
      description='Static Website Builder',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Craig Howard',
      author_email='craig@seagrape.us',
      install_requires=[
          'mako',
          'markdown',
          'mdx_smartypants',
          'meta'],
      keywords='Markdown website builder',
      url='https://seagrape.us/thera.html',
      scripts=['thera.py'],
      license='MIT',
      )

