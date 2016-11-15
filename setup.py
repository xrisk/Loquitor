from setuptools import setup

py_modules = ['bot', 'skeleton']
setup(name='Loquitor',
      version='1.0',
      description='Chatbot for Stack Overflow',
      author='Ralph Embree',
      author_email='ralph.embree@brominator.org',
      url='https://github.com/ralphembree/Loquitor',
      packages=['Loquitor', 'Loquitor.scripts'],
      install_requires=['chatexchange', 'bs4', 'requests', 'BingTranslator', 'feedparser'],
      scripts=['loquitor'],
      package_data={'scripts': ['scripts/SUBSTITUTIONS.txt']},
      use_2to3=True,
)
