from setuptools import setup, find_packages


setup(
    name="microservices_common",
    version="0.0.28",
    author="Ali Zaidi",
    author_email="support@arrivy.com",
    description="",
    long_description="",
    url="https://github.com/arrivy-dev/microservices-python-common",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'google-cloud-error-reporting==1.5.2',
        'google-cloud-storage==1.43.0',
        'google-cloud-tasks==2.7.1',
        'flask==2.0.2',
    ]
)
