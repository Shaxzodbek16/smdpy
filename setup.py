from setuptools import setup, find_packages

setup(
    name="smdpy",
    version="1.0.0",
    author="Muxtorov Shaxzodbek",
    author_email="muxtorovshaxzodbek16@gmail.com",
    description="It is download videos and audios from social media. That is why it is called smdpy",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Shaxzodbek16/smdpy",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        'requests',
        'yt-dlp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
