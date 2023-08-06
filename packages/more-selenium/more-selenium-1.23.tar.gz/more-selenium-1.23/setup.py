try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="more-selenium",
    version=1.23,
    author="Max",
    author_email="max@max.max",
    description="Better functionality for selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],

    url="https://github.com/MasterGrand/selenium_utils",

    include_package_data=True,
    data_files=[
        ("audio", [
            "more-selenium/audio_processing/ffmpeg.exe",
            ]),
    ],

    python_requires='>2.7, <4',
    install_requires=[
        "selenium",
        "SpeechRecognition",
        "opencv-python",
        "protobuf==3.19",
    ],
)
