from setuptools import setup

py_modules = ['bot', 'skeleton']
setup(name='Loquitor',
      version='1.0',
      description='Chatbot for Stack Overflow',
      author='Ralph Embree',
      author_email='ralph.embree@brominator.org',
      url='https://github.com/ralphembree/Loquitor',
      packages=['Loquitor', 'Loquitor.scripts'],
      install_requires=['BingTranslator', 'feedparser', 'ChatExchange6'],
      dependency_links=['http://github.com/ByteCommander/ChatExchange6/tarball/master#egg=ChatExchange6-1.0'],
      scripts=['bin/loquitor'],
      package_data={'scripts': ['scripts/SUBSTITUTIONS.txt']},
)
