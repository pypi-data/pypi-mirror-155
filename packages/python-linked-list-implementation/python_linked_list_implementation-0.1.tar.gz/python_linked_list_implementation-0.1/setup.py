from setuptools import setup, find_packages

setup(
    name='python_linked_list_implementation',
    version='0.1',
    license='GNU General Public License v3.0',
    author="Ej Lungay",
    author_email='ejlunday@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/noobfromph/python-linked-list.git',
    keywords='python linked list implementation',
    install_requires=[]
)