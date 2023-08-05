from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='terragit',
  version='0.3.6',
  description='terragit package',
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  url='https://gitlab.com/commons-acp/python/terraform-gitlab',
  author='aminnn',
  author_email='trabelsiamin9@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='terragit',
  packages=find_packages(),
  install_requires=[''],
    entry_points = ({
          'console_scripts': [
              'terragit = terragit.__main__:main'
          ]
      })
)
