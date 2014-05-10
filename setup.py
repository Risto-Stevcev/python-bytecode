from setuptools import setup, find_packages


setup(
    name='pybytecode',
    version='0.1',
    license='BSD',
    author='Risto Stevcev',
    author_email='risto1@gmail.com',
    url='https://github.com/Risto-Stevcev/pybytecode',
    description="A Python bytecode compiler and bytecode generator.",
    long_description=open("README.md","r").read(),
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['pybytecode=pybytecode.bytecode:main',
                            'pycodegen=pybytecode.codegen:main'],
    },
    keywords = "compiler bytecode python code",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Assemblers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Disassemblers',
        ],
)

