from setuptools import setup, find_packages
  
long_description = 'Some handy tools'
  
setup(
        name ='TheBatman',
        version ='0.0.1',
        author ='Harish PVV',
        author_email ='harishpvv@gmail.com',
        description ='Some handy tools',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='harishpvv',
        install_requires = [],
        zip_safe = False
)
