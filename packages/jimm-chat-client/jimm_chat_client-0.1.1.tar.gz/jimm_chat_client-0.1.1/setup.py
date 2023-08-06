from setuptools import setup, find_packages

setup(name="jimm_chat_client",
      version="0.1.1",
      description="Jimm Chat Client",
      author="Vyacheslav Fedorychev",
      author_email="nezl0i@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
