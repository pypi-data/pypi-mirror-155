from setuptools import setup, find_packages

setup(name="messenger_server_app",
      version="0.0.1",
      description="Messenger Server",
      author="Minor Anatolii",
      author_email="anminor91@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
