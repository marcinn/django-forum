from setuptools import setup, find_packages

setup(
    name='django-forum',
    version='0.1.0',
    description='Simple Django Forum Component',
    author='Ross Poulton',
    author_email='ross.poulton@gmail.com',
    url='http://code.google.com/p/django-forum/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
    setup_requires=['setuptools_git'],
)
