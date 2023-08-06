from setuptools import setup, find_packages

setup(
    name='apclib',
    version='0.0.3',
    license='MIT',
    author="Marnus Olivier",
    author_email='mo@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/MarnusOlivier/apcsim',
    keywords='apcsim',
    install_requires=["matplotlib","numpy","pandas","scipy","seaborn",],
)