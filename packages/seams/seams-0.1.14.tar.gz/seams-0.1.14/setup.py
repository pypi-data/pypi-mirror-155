from distutils.core import setup
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  name = 'seams',         
  packages = ['seams'],   
  version = '0.1.14',      
  license='',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A python SDK for the Seams API',  
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'David Bickford',                   
  author_email = 'dbickford@rjleegroup.com',   
  url = 'https://github.com/user/reponame',  
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',   
  keywords = ['seams', 'seam', 'rjlg', 'rjleegroup', 'rjlee'],   
  install_requires=[           
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers',    
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)