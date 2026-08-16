from setuptools import setup
import os
from glob import glob


package_name = 'restaurant_bot'


setup(
    name=package_name,
    version='0.0.0',

    packages=[package_name],

    data_files=[

        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        ('share/' + package_name, 
            ['package.xml']),


        # launch files
        (
        os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py')
        ),


        # worlds
        (
        os.path.join('share', package_name, 'worlds'),
        glob('worlds/*.world')
        ),

        # models
        (
        os.path.join('share', package_name, 'models'),
        glob('models/**/*', recursive=True)
        ),

    ],

)
