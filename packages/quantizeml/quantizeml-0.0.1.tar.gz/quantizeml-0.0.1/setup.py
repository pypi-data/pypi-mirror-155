from os import path
from setuptools import setup, find_packages

# Read the contents of the README file
directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='quantizeml',
      version='0.0.1',
      description='Base layers and calibration/quantization tools',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='David Corvoysier',
      author_email='dcorvoysier@brainchip.com',
      url='https://doc.brainchipinc.com',
      license='Apache 2.0',
      license_files=['LICENSE'],
      packages=find_packages(),
      entry_points={},
      install_requires=['tensorflow~=2.8.0', 'keras~=2.8.0', 'numpy'],
      python_requires='>=3.7')
