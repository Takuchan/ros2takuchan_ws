from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'megarover_sim'

setup(
    name=package_name,
    version='0.0.2',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/launch/utils', glob('launch/utils/*.py')),
        ('share/' + package_name + '/urdf', glob('urdf/*.xacro')),
        ('share/' + package_name + '/urdf', glob('urdf/*.gazebo')),
    ('share/' + package_name + '/meshes/mega3', glob('meshes/mega3/*.stl')),  
        ('share/' + package_name + '/worlds/gz', glob('worlds/gz/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Takuchan',
    maintainer_email='takuchanapp@gmail.com',
    description='Megarover3をGazeboで動かすROS2シミュレーションパッケージ',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'master = megarover_sim.master:main'
        ],
    },
)
