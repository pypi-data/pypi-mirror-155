from setuptools import setup, find_packages

setup(
    name="Py-Github-9045",
    version='1.0',
    license='MIT',
    author="Henish Patel",
    author_email='ompatel9045@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/henishpatel9045/GitHubAPI',
    keywords='GitHubAPI RestApi Python',
    install_requires=[
          'requests',
          'pynacl'
      ],
)
