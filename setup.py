from setuptools import setup

py_modules = ['bot', 'skeleton']
setup(name='Loquitor',
      version='1.0',
      description='Chatbot for Stack Overflow',
      author='Ralph Embree',
      author_email='ralph.embree@brominator.org',
      url='https://github.com/ralphembree/Loquitor',
      packages=['Loquitor', 'Loquitor.scripts'],
      install_requires=['bs4', 'requests', 'BingTranslator', 'feedparser'],
      dependency_links=['https://github.com/ByteCommander/ChatExchange6/tarball/master#egg=ChatExchange6'],
      scripts=['loquitor'],
      package_data={'scripts': ['scripts/SUBSTITUTIONS.txt']},
)
