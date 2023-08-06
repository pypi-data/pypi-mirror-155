from setuptools import setup, find_packages
setup(name="milvusCompute",
      version='0.0.1',
      description="milvus connect, insert and search base package",
      author="jessicaqi",
      autho_email='jessicaqi556@hotmail.com',
      requires=['pymilvus'],
      packages=find_packages(),
      license='apache 3.0')