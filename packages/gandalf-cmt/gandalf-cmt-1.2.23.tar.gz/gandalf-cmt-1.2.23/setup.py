# -*- coding: utf-8 -*-

# python setup.py sdist
# twine upload dist/*

from setuptools import *


setup(
    name='gandalf-cmt',
    version='1.2.23',
    license='MIT',
    description="Gandalf is a Configuration Management tool.",
    maintainer="Arjun Babu",
    maintainer_email='arbnair97@gmail.com',
    author="Arjun Babu",
    author_email='arbnair97@gmail.com',
    include_package_data=True,
    packages=['src', 'modules'],
    package_dir={'src': 'src', 'modules': 'src/modules'},
    package_data={'src': ['src/gandalf'], 'modules': ['src/modules/*.py']},

    data_files=[
        ('Lib/gandalf-cli', ['src/gandalf']),
        ('Lib/gandalf-cli/modules', ['src/modules/bedcCUModule.py', 'src/modules/pipelineIncrement.py', 'src/modules/bedcMGMTModule.py'])],


    keywords='gandalf-cmt',
    install_requires=[
          'numpy',
          'pathlib'
      ],
    
    classifiers=[
          'Development Status :: 4 - Beta'
          ],

)

