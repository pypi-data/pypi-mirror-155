from setuptools import setup, find_packages

req = []
with open("venv_requirements.txt") as f:
    for l in f.readlines():
        req.append(l[:-1])
setup(
    name='apclib',
    version='0.0.2',
    license='MIT',
    author="Marnus Olivier",
    author_email='mo@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/MarnusOlivier/apcsim',
    keywords='apcsim',
    install_requires=req,
)