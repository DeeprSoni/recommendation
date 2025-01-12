from setuptools import setup, find_packages

setup(
    name='ai-recommender',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=1.0',
        'numpy>=1.21',
        'pandas>=1.3'
    ],
    description='A vector-based AI recommendation system built using scikit-learn.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    license='MIT',
    url='https://github.com/your_username/ai-recommendation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)