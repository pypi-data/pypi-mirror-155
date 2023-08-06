from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from pathlib import Path


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # check_call(f"{sys.path[0]}{os.sep}postinstall{os.sep}install.py")
        install.run(self)


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='pynibs',
      version='0.1.6',
      description='A python toolbox to conduct non-invasive brain stimulation experiments (NIBS).',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Konstantin Weise, Ole Numssen',
      author_email='kweise@cbs.mpg.de',
      package_data={'pynibs.pckg': ['biosig/biosig4c++-1.9.5.src_fixed.tar.gz']},
      keywords=['NIBS', 'non-invasive brain stimulation', 'TMS', 'FEM'],
      include_package_data=True,
      project_urls={'Home': 'https://gitlab.gwdg.de/tms-localization/pynibs',
                    'Docs': 'https://pynibs.readthedocs.io/',
                    'Download': 'https://pypi.org/project/pynibs/'},

      license='GPL3',
      packages=['pynibs',
                'pynibs.exp',
                'pynibs.models',
                'pynibs.util',
                'pynibs.pckg'],
      install_requires=['dill',
                        'h5py',
                        'lmfit',
                        'matplotlib',
                        'numpy',
                        'nibabel',
                        'pandas',
                        'pygpc',
                        'pyyaml',
                        'scipy',
                        'scikit-learn',
                        'packaging',
                        'lxml',
                        'tables',
                        'tqdm',
                        'pillow',
                        'fslpy',
                        'mkl',
                        'trimesh',
                        'fmm3dpy',
                        'tvb-gdist',
                        'ortools<=9.1.9490'],
      python_requires='>=3.7',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Build Tools',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9', ],

      zip_safe=False,
      cmdclass={
          'develop': PostDevelopCommand,
          'install': PostInstallCommand,
      }, )
