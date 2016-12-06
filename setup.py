from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='chwrapper',
      version='0.3.0',
      description='A simple wrapper around the Companies House API',
      long_description=readme(),
      url='http://github.com/jamesgardiner/chwrapper',
      author='James Gardiner',
      author_email='jamesg87@me.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'requests==2.8.1',
      ],
      classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
      ])
