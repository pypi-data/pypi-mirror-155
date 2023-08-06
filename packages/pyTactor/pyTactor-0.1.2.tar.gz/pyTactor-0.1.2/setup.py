from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(name='pyTactor',
      version='0.1.2',
      url='https://github.com/Munroe-Meyer-Institute-VR-Laboratory/pyTactor',
      author='Walker Arce',
      author_email='walker.arce@unmc.edu',
      description='Control a vibrotactor array over BLE using Python code.',
      keywords='BLE vibrotactor',
      long_description=readme,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8'
      ],
      long_description_content_type="text/markdown",
      zip_safe=False,
      license='MIT',
      include_package_data=True,
      packages=['pytactor'],
      install_requires=[
            'adafruit-blinka-bleio',
            'adafruit-circuitpython-ble'
      ],
      )

# python setup.py bdist_wheel
# pip3 install pdoc3
# pdoc --html --output-dir docs pywoodway
# https://ftdichip.com/drivers/
