import setuptools
import bdating_common
with open("README.md") as fp:
  long_description = fp.read()

setuptools.setup(
    name="bdating-common",
    version=bdating_common.__version__,

    description="Bdating common libraries standard library",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Zac",
    author_email="zac@bdating.io",
    package_dir={"": "."},
    packages=setuptools.find_packages(),
    package_data={'': ['data/*', '*.cer']},
    url='https://github.com/bdating-io/bdating-python-common',
    install_requires=[
        "boto3<2",
        "click-log<0.4",
        "click<8.0",
        "dnspython==2.2.0",
        "PyMySQL"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    entry_points={
        'console_scripts': [
            'report-metrics=bdating_common.report_metrics:report',
            'report-events=bdating_common.report_events:report'
        ],
    }
)
