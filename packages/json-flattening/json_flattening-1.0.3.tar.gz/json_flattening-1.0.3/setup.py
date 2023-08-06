from setuptools import setup, find_packages

classifiers =[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent']


setup(
    name='json_flattening',
    version='1.0.3',
    author='Rahul Goel',
    description = 'Package to Flatten JSON data to relational Dataframe',
    long_description_content_type='text/markdown',
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/rahulgoel11/json_flattening',
    license='MIT',
    packages=find_packages(),
    classifiers = classifiers,
    keywords='json flatten',
    install_requires=[
          'pandas','numpy'
      ],

)