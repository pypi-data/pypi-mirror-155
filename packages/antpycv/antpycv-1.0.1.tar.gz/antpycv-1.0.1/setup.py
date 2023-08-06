from setuptools import setup
setup(name='antpycv',
      description='Arduino Helper Library',
      author='Kakada Sam',
      author_email='sam.kakada@gmail.com',
      license='MIT',
      version='1.0.1',
      install_requires=[
        'opencv-python==4.6.0.66',
        'numpy==1.21.6',
        'pyserial==3.5',
        'mediapipe==0.8.10',
        'msvc-runtime==14.29.30133',
        'protobuf==3.19.0'
      ],
      packages=['antpycv'],
      zip_safe=False,
      classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',  #pyhton versions that work well for Arduino
    ],
      )