from setuptools import setup, find_packages

classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]

setup(
        name                 = 'funcaptcha',
        version              = '0.1.2',
        description          = 'Funcaptcha API',
        author               = 'Tekky',
        author_email         = 'xtekky@protonmail.com',
        url                  = 'https://pypi.org/project/funcaptcha/',
        packages             = find_packages(),
        license              = 'MIT',
        install_requires     = ['requests'], #, 'certify', 'idna', 'Pillow', 'pycryptodome', 'PyExecJS', 'urllib3', 'charset-normalizer', 'six'],
        include_package_data = True
    )