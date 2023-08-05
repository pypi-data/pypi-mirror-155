from setuptools import setup, find_packages

classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]

description = """
# funcaptcha
#### Status ~ under developement
#### Repository: [github.com/xtekky/funcaptcha](https://gihub.com/xtekky/funcaptcha)
## install funcaptcha
```
pip install funcaptcha
```
## current example (get key)
```python
from funcaptcha import Funcaptcha

funcap = Funcaptcha(
    api_url  = 'twitch-api.arkoselabs.com',
    api_key  = 'E5554D43-23CC-1982-971D-6A2262A2CA24',
    site_url = 'https://www.twitch.tv'
)

key = funcap.getkey()

print(f"Key: {key}")
```

Tekky (c) 2022
"""
setup(
        name                 = 'funcaptcha',
        version              = '0.1.4',
        description          = 'Funcaptcha API',
        author               = 'Tekky',
        author_email         = 'xtekky@protonmail.com',
        url                  = 'https://pypi.org/project/funcaptcha/',
        long_description     = description,
        long_description_content_type='text/markdown',
        packages             = find_packages(),
        license              = 'MIT',
        install_requires     = ['requests'], #, 'certify', 'idna', 'Pillow', 'pycryptodome', 'PyExecJS', 'urllib3', 'charset-normalizer', 'six'],
        include_package_data = True
    )