from setuptools import setup, find_packages

with open('requirements.txt') as requirements:
    setup(
        name="finx-io",
        description="FinX API SDK",
        version="0.0.4-dev-1",
        author="FinX Capital Markets LLC",
        author_email="info@finx.io",
        long_description="The FinX SDK is a collection of code that has interfaces to the FinX Capital Markets Analytics Platform (FinX CMAP). The code in the SDK makes calls to REST APIs & WebSocket endpoints. A FinX API Key is required for the SDK to return results.",
        long_description_content_type="text/x-rst",
        classifiers=[
            "License :: OSI Approved :: GNU Affero General Public License v3",],
        license="APGL3",
        package_dir={"": "src"},
        packages=find_packages(where="src", exclude=("*.tests",)),
        python_requires=">=3.6",
        url="https://github.com/FinX-IO/sdk",
        install_requires=[x.split(next((sep for sep in ['==', '>=', '<=', '~='] if sep in x), ''))[0]
                          for x in requirements.readlines()],
        # include_package_data is needed to reference MANIFEST.in
        include_package_data=True,
    )
