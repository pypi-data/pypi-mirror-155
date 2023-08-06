from setuptools import setup

readme = open("./README.md", "r")


setup(
    name="KrakenOS",
    packages=["KrakenOS"],  # this must be the same as the name above
    version="1.0.0.12",
    description='Optical Simulation and ray tracing',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='joel Herrera et al.',
    author_email='joel@astro.unam.mx',
    # use the URL to the github repo
    url='https://github.com/Garchupiter/Kraken-Optical-Simulator',
    download_url='https://github.com/Garchupiter/Kraken-Optical-Simulator',
    keywords=['Optical', 'Simulator', 'lens'],
    classifiers=[ ],
    license='GNU General Public License v3.0',
    include_package_data=True
)
