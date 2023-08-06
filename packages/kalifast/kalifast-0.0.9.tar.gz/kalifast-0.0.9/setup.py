from setuptools import setup, find_packages


setup(
    name='kalifast',
    version='0.0.9',
    license='MIT',
    author="EISGE",
    author_email='e@eisge.com',
    package_dir={'': 'src'},
    description="Python package for kalifast record npp plugin",
    install_requires=[
          'scikit-learn','pynput'
      ],

)