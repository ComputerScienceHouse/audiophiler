# File: setup.py
# Audiophiler flask app setup
# @author: Stephen Greene (sgreene570)


from setuptools import setup
setup(
    name="audiophiler",
    packages=["audiophiler"],
    include_package_data=True,
    install_requires=[
        'flask',
        'boto',
        'werkzeug',
        'flask-pyoidc',
    ],
)
