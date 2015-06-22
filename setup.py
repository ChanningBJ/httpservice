from setuptools import setup, find_packages

setup(
    name='httpservice',
    version='1.0',
    include_package_data=True,
    packages=find_packages(),
    url='',
    license='',
    author='chengmingwang',
    author_email='',
    description='Provides a easier interface for define http parameters, do parameter verification and generate API documents',
    data_files=[
        ('resources', ['resources/styles.css']),
        ('bin',['bin/rippledoc-0.1.1-standalone.jar'])
    ]
)
