#! /usr/bin/env python3


from setuptools import setup
setup(
    name='markdown-lightbox',
    version='2.0.0',
    author='K.D.Murray, originally Alicia Schep',
    author_email='foss@kdmurray.id.au',
    description='Markdown extension which turns images into lightbox',
    url='https://github.com/kdm9/markdown-lightbox',
    py_modules=['mdx_lightbox'],
    install_requires=['markdown>=3.0'],
    classifiers=[
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)




