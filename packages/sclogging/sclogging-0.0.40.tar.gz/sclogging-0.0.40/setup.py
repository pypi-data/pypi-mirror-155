from setuptools import setup, find_packages

setup(
    name='sclogging',
    version='0.0.40',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={'sclogging': ['config.py', 'settings.toml']},
    url='https://github.com/sshimek42/sclogging',
    license='MIT',
    author='',
    author_email='',
    description=''
    )
