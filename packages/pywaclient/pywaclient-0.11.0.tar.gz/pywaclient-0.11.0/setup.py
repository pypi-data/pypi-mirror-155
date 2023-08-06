import setuptools

with open('README.md', 'r') as fp:
    setuptools.setup(
        name="pywaclient",
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        author="Jonas Waeber",
        author_email="jonaswaeber@gmail.com",
        description="A small wrapper library around the World Anvil Aragorn API: "
                    "https://www.worldanvil.com/api/aragorn/documentation.",
        long_description=fp.read(),
        long_description_content_type="text/markdown",
        url="https://gitlab.com/SoulLink/world-anvil-api-client",
        packages=['pywaclient', 'pywaclient.endpoints', 'pywaclient.models', 'pywaclient.exceptions'],
        install_requires=['requests'],
        license='Apache 2.0',
        classifiers=[
            "Programming Language :: Python :: 3.7"
        ],
    )
