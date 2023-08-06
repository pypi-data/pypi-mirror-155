from distutils.core import setup
setup(
  name = 'yungestWeb',         
  packages = ['yungestWeb'],   
  version = '0.0.2',      
  license='MIT',        
  description = 'TYPE YOUR DESCRIPTION HERE',   
  author = 'yungestDev',                   
  author_email = 'yungestmonsterhahaha@gmail.com',      
  #url = 'https://github.com/user/reponame',   
  #download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   
  install_requires=[            
          'wsgiref',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.10',      

  ],
)