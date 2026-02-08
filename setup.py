"""
Setup configuration for the backend package
"""

from setuptools import setup, find_packages

setup(
    name='content-recommender',
    version='1.0.0',
    description='Content Recommendation System using TF-IDF and Cosine Similarity',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'flask>=3.0.0',
        'flask-cors>=4.0.0',
        'mysql-connector-python>=8.2.0',
        'PyJWT>=2.8.0',
        'bcrypt>=4.1.2',
        'scikit-learn>=1.3.2',
        'pandas>=2.1.4',
        'numpy>=1.26.2',
        'python-dotenv>=1.0.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)