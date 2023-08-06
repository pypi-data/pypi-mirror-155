from setuptools import setup, find_packages
install_requires = ['numpy','scipy']
setup(
    name = 'cg2at',
    version='2022.6.16',
    author='owenvickery, Aunity',
    author_email='maohuay@hotmail.com',
    description=('Converts CG representation into an atomistic representation'),
    url='https://github.com/Aunity/cg2at',
    license='GPL-3.0 License',
    keywords='CG',
    install_requires=install_requires,
    packages=find_packages(),
    zip_safe = False,
    #packages=packages,
    entry_points={'console_scripts': [
         'cg2at = cg2at.bin.cg2at:main',
     ]},
    include_package_data=True
)
