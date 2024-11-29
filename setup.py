from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='demo-flask-vuejs-rest',
        version='0.0.1',
        packages=find_packages(),
        scripts=["./streamde"],
    )
