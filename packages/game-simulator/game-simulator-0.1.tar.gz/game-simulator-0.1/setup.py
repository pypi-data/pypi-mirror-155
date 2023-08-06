from distutils.core import setup

setup(
  name = 'game-simulator',         
  packages = ['game_simulator'],   
  version = '0.1',      
  license='MIT',        
  description = 'Creates simulations of any n*n game specified with payoff matrix',   
  author = 'ankurtutlani',                   
  author_email = 'ankur.tutlani@gmail.com',      
  url = 'https://github.com/ankur-tutlani/game-simulator',   
  download_url = 'https://github.com/ankur-tutlani/game-simulator/archive/refs/tags/v_01.tar.gz',    
  keywords = ['game theory', 'evolutionary game', 'social norms','multi-agents','evolution','Nash equilibrium'],   
  install_requires=[            
          'numpy',
		  'pandas'
		  
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
												
	'Programming Language :: Python :: 3.7',
  ],
)