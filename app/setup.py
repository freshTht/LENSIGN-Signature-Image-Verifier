from setuptools import setup

setup(
    name='lensign',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)