from setuptools import setup

setup(
    name='inventory_service',
    packages=['inventory_service'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests'
    ],
)
