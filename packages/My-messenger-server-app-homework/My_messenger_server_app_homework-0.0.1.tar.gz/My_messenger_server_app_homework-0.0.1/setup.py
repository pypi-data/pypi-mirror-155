from setuptools import setup, find_packages

setup(name="My_messenger_server_app_homework",
      version="0.0.1",
      description="Серверверная часть приложения 'My messanger' для обмена сообщениями. Практика учебной части",
      author="Roman Melnikov",
      author_email="tupozarabotok@gmail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
