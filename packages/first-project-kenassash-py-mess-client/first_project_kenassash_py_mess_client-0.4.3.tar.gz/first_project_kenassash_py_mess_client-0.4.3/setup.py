from setuptools import setup, find_packages

setup(name="first_project_kenassash_py_mess_client",
      version="0.4.3",
      description="Mess Client",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
