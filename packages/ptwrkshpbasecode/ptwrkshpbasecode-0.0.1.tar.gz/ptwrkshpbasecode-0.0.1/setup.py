from setuptools import find_packages, setup  # type: ignore

setup(
    name="ptwrkshpbasecode",
    version="0.0.1",
    description="temp package for workshop",
    author="",
    author_email="",
    long_description="temp package for workshop",
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pt-workshop=ptwrkshpbasecode.client.ptwrkshpclient:main"
        ],
    },
    install_requires=["azure.identity", "aiohttp", "Click", 'azure.storage.blob'],
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "mypy"]
    },
)
