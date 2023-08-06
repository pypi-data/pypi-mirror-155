from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()
    readme_file.close()

requirements = ["requests==2.27.1", "docker==5.0.3"]

setup(
    name="metrograph",
    version="0.0.1",
    author="Hamza EL GARRAB",
    author_email="hamza.elgarrab@gmail.com",
    description="Metrograph's core official package",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/metrograph/metrograph-core",
    packages=find_packages(),
    install_requires=requirements,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
)