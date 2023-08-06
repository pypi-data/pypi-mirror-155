from setuptools import setup, find_packages

setup(name="messenger_client_from_nadezhda",
      version="0.2.0",
      description="Client packet",
      author="Nadezhda Vlasova",
      author_email="nadvlasova@rambler.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
