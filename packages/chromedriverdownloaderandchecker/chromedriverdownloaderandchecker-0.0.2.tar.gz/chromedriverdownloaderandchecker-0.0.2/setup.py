from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='chromedriverdownloaderandchecker',
    version='0.0.2',
    description='Simple chromedriver downloader and checker',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Hrithik Joshi V',
    author_email='hrithikjoshi987@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='python, selenium',
    packages=find_packages(),
    install_requires=['']
)