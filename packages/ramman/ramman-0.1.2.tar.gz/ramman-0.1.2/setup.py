from setuptools import setup

INSTALL_REQUIRES = ['requests', 'click']

setup(
    name='ramman',
    version='0.1.2',
    packages=['ramman'],
    url='http://www.somenergia.coop',
    license='MIT',
    install_requires=INSTALL_REQUIRES,
    entry_points="""
    """,
    author='Somenergia, coop',
    author_email='',
    description='Heman tiny client'
)
