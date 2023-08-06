from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-tools',
    version=version,
    description='Talisman applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['talisman_tools', 'talisman_tools.*']),
    install_requires=[
        'talisman-dm>=0.4.5', 'talisman-interfaces',
        'fastapi>=0.73.0', 'python-multipart>=0.0.5', 'requests>=2.22.0', 'uvicorn>=0.13.3', 'jsonformatter>=0.3.0'
    ],
    extras_require={
        'logstash': ['python3-logstash>=0.4.80']
    },
    entry_points={
        'console_scripts': [
            'talisman-tools = talisman_tools.talisman:main',
        ]
    },
    data_files=[('', ['VERSION'])],
    python_requires='>=3.6',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
