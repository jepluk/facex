import os, shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)

        src_file = os.path.join(os.path.dirname(__file__), 'my_package', 'file_yang_ingin_disalin')
        dest_dir = '/data/data/com.termux/files/usr/bin/'
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy(src_file, dest_dir)

setup(
    name='facex',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'facex=facex.cli:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
