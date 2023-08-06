from setuptools import setup, find_packages

setup(name='nakama-python',
      version='1.0.3',
      description='Python client for Nakama server',
      packages=find_packages(),
      license='MIT',
      author='Bernard Ojengwa',
      author_email='bernardojengwa@gmail.com',
      url='https://github.com/ojengwa/nakama-python',
      keywords='nakama',
      install_requires=['aiohttp', 'asyncio'],
      zip_safe=False)
