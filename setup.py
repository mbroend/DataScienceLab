
from distutils.core import setup
import DataScienceLab as dsl
ver = dsl.__version__

setup(
  name = 'DataScienceLab',         # How you named your package folder (MyLib)
  packages = ['DataScienceLab'],   # Chose the same as "name"
  version = ver,      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Building blocks for common data science work',   # Give a short description about your library
  author = 'Mathias Brønd Sørensen',                   # Type in your name
  author_email = 'mathias.b.sorensen@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/mbroend/DataScienceLab/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/mbroend/DataScienceLab/archive/v_'+ver[0]+ver[2:]+'.tar.gz',    # release URL
  keywords = ['data science', 'SQL', 'SERVER', 'CONNECTION', 'SIMPLIFIED', 'machine learning'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pyodbc',
          'sqlalchemy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)