from setuptools import setup, find_packages


setup(
    name='bot-assistant',
    version='0.2.4',
    license='MIT',
    author="Soukarja Dutta",
    author_email='soukarjadutta@gmail.com',
    packages=find_packages('botAssistant'),
    package_dir={'': 'botAssistant'},
    url='https://github.com/soukarja/botAssistant_Python',
    keywords='example project',
    install_requires=[
          'selenium'
      ]

)