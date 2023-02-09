from pathlib import Path
from setuptools import find_packages
from setuptools import setup


root_dir = Path(__file__).parent
readme_content = (root_dir / 'README.md').read_text()

setup(
    name='offsettmpsubs',
    version='1.0.0',
    description='A cli tool for delaying/hastening subtitles in stored in TMP '
                'format.',
    license='MIT License',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    author='Piotr Momot',
    author_email='waizer12@gmail.com',
    url='https://github.com/luciferDisciple/offsettmpsubs',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='>=3.8',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'offsettmpsubs=offsettmpsubs:main'
        ]
    }
)
