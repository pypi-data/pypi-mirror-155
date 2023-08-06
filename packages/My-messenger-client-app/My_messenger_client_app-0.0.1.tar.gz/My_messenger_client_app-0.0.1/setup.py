from setuptools import setup, find_packages

setup(name="My_messenger_client_app",
      version="0.0.1",
      description="Клиентская часть приложения 'My messanger' для обмена сообщениями. Практика учебной части",
      author="Roman Melnikov",
      author_email="tupozarabotok@gmail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
