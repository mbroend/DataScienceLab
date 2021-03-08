
from distutils.core import setup
setup(
  name = 'DataScienceLab',         # How you named your package folder (MyLib)
  packages = ['DataScienceLab'],   # Chose the same as "name"
  version = '0.1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Building blocks for common data science work',   # Give a short description about your library
  author = 'Mathias Brønd Sørensen',                   # Type in your name
  author_email = 'mathias.b.sorensen@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/mbroend/DataScienceLab/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/mbroend/DataScienceLab/archive/v_01.3.tar.gz',    # I explain this later on
  keywords = ['data science', 'SQL', 'SERVER', 'CONNECTION', 'SIMPLIFIED'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'sqlalchemy',
          'pyodbc'
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