from setuptools import setup, find_packages

setup(name='ecgxai',
      version='0.1.0',
      description='Neatly packaged AI methods for ECG analysis',
      author='Rutger van de Leur',
      author_email='r.r.vandeleur@umcutrecht.nl',
      license='GNU AGPLv3',
      packages=find_packages(include=['ecgxai', 'ecgxai.*']),
      url="https://github.com/rutgervandeleur/ecgxai",
      install_requires=[
          "pytorch_lightning==1.5.10",
          "torchmetrics==0.9.1",
          "torch==1.9.*",
          "numpy",
          "scipy",
          "pandas",
          "scikit-learn",
          "tqdm"
        ])