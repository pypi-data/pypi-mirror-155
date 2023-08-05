from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tf_cli",
    version="0.0.9",
    description="This contains a CLI for AWS terraform",
    author="Rooklyn Kline",
    author_email="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rkline2/tf_cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={'':['scripts/*.sh']},
    #include_package_data=True,
    #data_files=[('lib/python3.8/site-packages/tf/scripts',['src/tf/scripts/build.sh', 'src/tf/scripts/clean.sh', 'src/tf/scripts/commit.sh', 'src/tf/scripts/push.sh'])],
    install_requires=["click==8.1.3", "wheel==0.37.0"],
    entry_points = {
        'console_scripts':[
            'tf = tf.cli:main',
        ],
    },
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "pytest==6.2.5",
            "wheel==0.37.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
    ]
)
