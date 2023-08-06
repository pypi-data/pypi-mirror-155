import setuptools
    
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='jira_easy_api',
    version='0.1.2',
    author='DovaX',
    author_email='dovax.ai@gmail.com',
    description='A wrapper around Jira API to run jira commands missing in their UI as oneliners',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DovaX/jira_easy_api',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          ['jira']
     ],
    python_requires='>=3.6',
)
    