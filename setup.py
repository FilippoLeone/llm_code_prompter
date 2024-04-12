from setuptools import setup, find_packages

setup(
    name='LLM_Code_Prompter',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.7',
        'tiktoken==0.6.0',
        'pywin32==306'
    ],
    entry_points={
        'console_scripts': [
            'llm_code_prompter=src.main:main',
        ],
    },
    author='',
    author_email='',
    description='A utility to generate structured prompts for GPT-4 using project files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
