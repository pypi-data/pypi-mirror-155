from setuptools import setup, find_packages


setup(
    name='benzene_translator',
    version='0.1',
    license='MIT',
    author="Viswanathan S",
    author_email='vichusathappan@gxample.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='translator',
    install_requires=[
          'json', 'requests', 'random', 're','retry',
      ],)
