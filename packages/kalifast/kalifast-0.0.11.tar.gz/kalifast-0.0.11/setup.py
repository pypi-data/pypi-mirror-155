from setuptools import setup, find_packages


setup(
    name='kalifast',
    version='0.0.11',
    license='MIT',
    author="EISGE",
    author_email='e@eisge.com',
    packages=['kalifast'],
    description="Python package for kalifast record npp plugin",
    install_requires=
    [
        'mpi4py>=2.0',
        'numpy',                     
    ],
    # install_requires=[
    #      'pynput','shutil','tempfile','datetime','tkinter','turtle'
    #   ],

)