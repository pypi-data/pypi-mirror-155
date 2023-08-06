from setuptools import setup, find_packages


setup(
   name='honeycheck',
   version='0.2.0',
   author='Samuel López Saura',
   author_email='samuellopezsaura@gmail.com',
   packages=find_packages(),
   license='MIT',
   url='https://github.com/elchicodepython/HoneyCheck',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='Honeycheck detects rogue dhcp servers and provides a modular and fully configurable action environment in case they are found',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "scapy-python3==0.20",
   ],
)
