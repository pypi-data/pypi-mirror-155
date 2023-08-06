from distutils.core import setup
import setuptools

def readme():
    with open(r'README.txt') as f:
        README = f.read()
    return README

setup(
    name = 'seopy', ###################################
    packages = setuptools.find_packages(),

    version = '1.1',
    license='MIT',
    description = 'Instantly analyze your SEO issues',
    author = 'Dhiraj Beri',
    author_email = 'dhirajberi.official@gmail.com',
    url = 'https://github.com/dhirajberi/seopy',
    download_url = 'https://github.com/dhirajberi/seopy/archive/refs/tags/1.1.tar.gz',
    keywords = ['seo', 'seopy'],
    install_requires=[
          'selenium',
          'webdriver_manager', 
      ],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    ],
)
