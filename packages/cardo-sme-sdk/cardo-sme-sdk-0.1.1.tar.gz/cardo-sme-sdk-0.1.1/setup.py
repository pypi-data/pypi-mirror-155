with open('README.md', 'r') as f:
    long_description = f.read()

from setuptools import setup, find_packages

setup(
    name='cardo-sme-sdk',
    version='0.1.1',
    description='SME Service SDK in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://docs.service.cardoai.com/sme_sdk/index.html',
        'Source': 'https://github.com/CardoAI/sme_python',
    },
    author='Klement Omeri',
    author_email='hello@cardoai.com',
    license='MIT',
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=[
        'boto3>=1.20.27',
        'requests>=2.27.1'
    ],
    extras_require={
        'dev': [
            'pytest>=7',
            'pytest-cov>=3',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
