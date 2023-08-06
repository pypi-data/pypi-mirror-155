from distutils.core import setup
"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author='Alex Vasi, Wang, Richard',
    author_email='richardwangwang@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A simple menu for Django",
    install_requires=requirements,
    license='BSD',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='simplemenu',
    name='django-simplemenu-simplified',
    packages=['simplemenu', 'simplemenu.templatetags'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/weijia/django-simplemenu',
    version='2.0.1',
    zip_safe=False,
)

