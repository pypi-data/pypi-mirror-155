from setuptools import setup, find_packages


setup(
    name='trebu',
    version='0.6',
    license='MIT',
    author="Antonio Longoria",
    author_email='antonio@trebu.io',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='Trebu SDK',
    install_requires=[
          'numpy',
      ],

)
