from setuptools import setup, find_packages

setup(name="first_project_kenassash_py_mess_server",
      version="0.4.4",
      description="Mess Server",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
