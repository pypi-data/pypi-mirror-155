from setuptools import setup, find_packages


setup(
    name='meme-python',
    version='1.0.0',
    license='MIT',
    author='Gabe Millikan',
    url='https://github.com/GabeMillikan/meme-python',
    install_requires=['Pillow'],
    python_requires='>=3',
    description='Meme Generator',
    long_description='Meme Generator. See [repository on Github](https://github.com/GabeMillikan/meme-python).',
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(include=['meme']),
    package_data={
        'meme': ['static/*'],
    },
)
