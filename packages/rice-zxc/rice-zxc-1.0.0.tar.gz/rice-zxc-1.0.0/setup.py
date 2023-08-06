from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='rice-zxc',
  version='1.0.0',
  description='Танцующий ASCII дед инсайд кот.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/meth1337/rice-zxc',
  author='meth1337',
  author_email='zx630c@mail.ru',
  license='MIT',
  classifiers=classifiers,
  keywords='rice ascii',
  packages=find_packages(),
  install_requires=['colorama']
)

