from setuptools import setup, find_packages


setup(
    name='cw-torch',
    version='0.1',
    license='MIT',
    author="Szymon Knop",
    author_email='szymonknop@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/EszKnop/cw-torch',
    keywords='cramerwold cwae lcw autoencoder cramer wold',
    install_requires=[
          'torch',
      ],

)