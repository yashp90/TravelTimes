from setuptools import setup

setup(name='TravelTimes',
      version='1.0',
      description='Travel Times',
      url='https://github.com/yashp90/TravelTimes',
      author='Yash P',
      author_email='yashp90@gmail.com',
      license='MIT',
      packages=['traveltimes'],
      scripts=['bin/traveltimes'],
      install_requires=[
          'googlemaps',
          'requests',
          'schedule'
      ],
      zip_safe=False)
