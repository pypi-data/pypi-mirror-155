from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

setup(
    name='aurh',
    version='0.0.2',
    description='An AUR helper in Python.',
    keywords='arch aurh',
    author='Ajith',
    author_email='ajithar204@gmail.com',
    url='https://github.com/ajthr/aurh.git',
    license='MIT',
    long_description=long_description,
    platforms='Arch Linux',
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Topic :: System',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: Utilities'
    ],
    packages=['aurh'],
    install_requires=['click', 'pyalpm', 'requests', 'srcinfo'],
    entry_points={
        'console_scripts': [
            'aurh = aurh.__main__:main',
        ]
    },
)
