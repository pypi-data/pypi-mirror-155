from setuptools import find_packages, setup

install_requires = [
        'zeep >= 0.12.0',
        'pytz',
        'setuptools' # i.e. provides pkg_resources
]

setup(
        name='inema',
        version='0.8.6',
        description='A Python interface to the Deutsche Post Internetmarke and Warenpost International Online Franking',
        long_description=open('README.rst').read(),
        author='Harald Welte',
        author_email='hwelte@sysmocom.de',
        url='https://git.sysmocom.de/odoo/python-inema/',
        packages=['inema'],
        install_requires=install_requires,
        package_data={'inema': ['data/products.json',
                                'data/products-2022-07-01.json',
                                'data/formats.json']},
        license='AGPLv3',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Office/Business',
        ],
        entry_points={
            'console_scripts': [ 'frank = inema.frank:main' ]
        },
)
