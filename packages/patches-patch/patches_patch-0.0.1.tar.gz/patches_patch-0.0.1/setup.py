from setuptools import setup, find_packages

# Setting up
setup(
    name="patches_patch",
    version='0.0.1',
    author="Teodor Markov",
    author_email="<mail@teddymarkov.com>",
    description='Instruments for patches',
    long_description_content_type="text/markdown",
    long_description='Instruments for patches.',
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    keywords=['python', 'patch', 'custom'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
