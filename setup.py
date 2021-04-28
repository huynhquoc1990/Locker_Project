from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='Locker_Project',
    version='0.2.1',
    packages=['Locker_Project'],
    url='https://github.com/huynhquoc1990/Locker_Project.git',
    license='MIT',
    author='Huỳnh Tấn Quốc',
    author_email='huynhquoc1990@gamil.com',
    description='Locker_Project Load',
    #install_requires=["",""],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description

)
