from setuptools import setup
import pathlib

"""
Can install dependencies directly by running from within this folder:
> pip install .
"""

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='xdat',
    version='0.1.44',
    description='eXtended Data Analysis Toolkit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/hermetric/xdat/',
    author='Ido Carmi',
    author_email='ido@hermetric.com',
    license='MIT',
    packages=['xdat'],
    install_requires=['pandas',
                      'numpy',
                      'scikit-learn',
                      'scriptinep3',
                      # 'pystan<3',
                      'tqdm',
                      'joblib',
                      'cloudpickle',
                      'matplotlib',
                      'pandas-sets',
                      'python-slugify',
                      # 'accupy',  # requires > sudo apt -q -y install libeigen3-dev
                      # 'tensorflow>=2',
                      'seaborn',
                      'missingno',
                      'data-science-utils',
                      'munch',
                      'arviz',
                      'python-pptx',
                      'feature_engine',
                      'case-converter'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
