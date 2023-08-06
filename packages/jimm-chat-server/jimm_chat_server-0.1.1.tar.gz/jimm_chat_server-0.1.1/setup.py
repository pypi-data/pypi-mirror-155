from setuptools import setup, find_packages

setup(name="jimm_chat_server",
      version="0.1.1",
      description="Jimm Chat Server",
      author="Vyacheslav Fedorychev",
      author_email="nezl0i@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      # scripts=['server/server_run']
      )
