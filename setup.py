import codecs
import os
from setuptools import setup, find_packages
import subprocess

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))


def get_desc():
    """Get long description by converting README file to reStructuredText."""
    file_name = os.path.join(LOCAL_PATH, 'README.md')
    if not os.path.exists(file_name):
        return ''

    try:
        cmd = "pandoc --from=markdown --to=rst %s" % file_name
        stdout = subprocess.STDOUT
        output = subprocess.check_output(cmd, shell=True, stderr=stdout)
        return output.decode('utf-8')
    except subprocess.CalledProcessError:
        print('pandoc is required for package distribution but not installed')
        return codecs.open(file_name, mode='r', encoding='utf-8').read()


def get_version():
    with codecs.open(os.path.join(LOCAL_PATH, 'favesdump.py'), 'r') as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip(' \'"')


setup(
    name='favesdump',
    description='last.fm faves dumper.',
    version=get_version(),
    license='MIT',
    author='Alex Musayev',
    author_email='alex.musayev@gmail.com',
    url='https://github.com/dreikanter/favesdump',
    long_description=get_desc(),
    platforms=['any'],
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'requests',
    ],
    entry_points={'console_scripts': ['favesdump = favesdump:main']},
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Utilities',
    ],
    dependency_links=[],
)
