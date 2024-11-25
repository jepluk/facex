import setuptools
import os
import shutil
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        
        target_path = '/data/data/com.termux/files/usr/bin/facex'
        source_path = os.path.join(os.path.dirname(__file__), 'facex/facex/cli.py')
        
        if not os.path.exists(target_path):
            shutil.copy(source_path, target_path)

setuptools.setup(
    author='Ipan (Nyett)',
    description='Facebook Bruteforce Attack.',
    entry_points={'console_scripts': ['facex=facex.cli:main']},
    install_requires=[
        'requests',
        'bs4'
    ],
    name='facex',
    packages=setuptools.find_packages(),
    cmdclass={
        'install': PostInstallCommand,  # Menggunakan kelas custom untuk post-install
    },
    version='1.0.0'
)

