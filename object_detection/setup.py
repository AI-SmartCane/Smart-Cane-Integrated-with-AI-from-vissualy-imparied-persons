from setuptools import setup

package_name = 'object_detection'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jc-bose-lab',
    maintainer_email='jc-bose-lab@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'testing_node = object_detection.testing_node:main',
            'camera_node = object_detection.camera_node:main',
            'tensorrt_node = object_detection.tensorrt_node:main',
            'servo_serial_node = object_detection.servo_serial_node:main',
        ],
    },
)
