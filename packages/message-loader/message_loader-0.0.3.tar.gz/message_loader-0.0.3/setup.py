from setuptools import setup, find_packages

# Setting up
setup(
    name="message_loader",
    version='0.0.3',
    author="Wxlbr73 (Will Ward)",
    # author_email="<me@gmail.com>",
    description='Basic Terminal Loading Message',
    long_description_content_type="text/markdown",
    long_description='Basic Loading Message Outputed to the Terminal with Animation',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'threading', 'loading'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# py setup.py sdist bdist_wheel
# twine upload dist/* --verbose
# Wxlbr73
# TwitchFan101
