from setuptools import setup, find_packages

setup(name="messenger_client_app",
      version="0.0.1",
      description="Messenger Client",
      author="Minor Anatolii",
      author_email="anminor91@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
