from setuptools import setup

setup(
    name='atms_api',
    version='1.10',
    packages=['atms_api'],
    url='',
    license='MIT',
    author='Glenn Vorhes',
    author_email='gavorhes@wisc.edu',
    description='Helper functions to interact with the WisDOT ATMS API',
    python_requires='>=3.3',
    install_requires=[
          'requests', 'typing', 'xmltodict', 'dicttoxml'
      ],
)
