from setuptools import setup

setup(
    name='twikitool',
    version='0.1',
    description='Helps with generating twiki pages',
    url='https://github.com/tklijnsma/twikitool.git',
    author='Thomas Klijnsma',
    author_email='thomasklijnsma@gmail.com',
    packages=['twikitool'],
    zip_safe=False,
    scripts=[
        'bin/twikitool',
        ],
    test_suite='nose.collector',
    tests_require=['nose'],        
    )