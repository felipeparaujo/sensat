from setuptools import find_namespace_packages, setup


setup(
    name="sensat",
    version="1.0",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "PyMySQL==0.9.3",
        "falcon==2.0.0",
        "aumbry[yaml]==0.10.0",
        "gunicorn==20.0.4"
    ],
    extras_require={
        "ci": [
            "pytest==5.3.5",
            "flake8==3.7.9"
        ]
    }
)
