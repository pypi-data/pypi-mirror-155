from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='get-btc-price',
  version='1.0.0',
  description='A python script that allows to get the current BTC price.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='meth1337',
  author_email='zx630c@mail.ru',
  license='MIT',
  classifiers=classifiers,
  keywords='btc',
  packages=find_packages(),
  install_requires=['requests']
)

