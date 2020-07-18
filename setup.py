from setuptools import setup, find_packages

setup(
    name='election2018',
    description='analyze president election in Russia 2018',
    version='0.0.1',
    author='Borodin Gregory',
    author_email='grihabor@gmail.com',
    email='https://github.com/grihabor/election2018',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['click', 'matplotlib'],
    entry_points={
        'console_scripts': ['election2018=election2018.cli:main'],
    }
)
