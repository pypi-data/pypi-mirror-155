# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlops_build']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'mlflow>=1.26.1,<2.0.0',
 'optuna>=2.10.0,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-multipart>=0.0.5,<0.0.6',
 'scikit-learn==1.1.1',
 'seaborn==0.11.2',
 'shap>=0.40.0,<0.41.0',
 'tqdm>=4.64.0,<5.0.0',
 'uvicorn>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['predict-model = mlops_build.predict_model:main',
                     'train-model = mlops_build.train_model:main',
                     'validate-model = mlops_build.validate_model:main']}

setup_kwargs = {
    'name': 'mlops-build',
    'version': '0.1.1',
    'description': 'MLops course',
    'long_description': '# ML-OPS',
    'author': 'gordeev.al',
    'author_email': 'aleksandr_gordeev2@epam.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gracikk-ds/ml-ops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
