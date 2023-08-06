import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name='daemondev_config_server',
        version='0.5',
        author='@daemondev',
        author_email='granlinux@gmail.com',
        description='Config-Files downloader',
        long_description=long_description,
        license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
        url = 'https://github.com/daemondev/daemondev-config-server',   # Provide either the link to your github or to your website
        long_description_content_type='text/markdown',
        #packages=setuptools.find_packages(),
        #packages = ['src/config_server'],   # Chose the same as "name"
        package_dir={"": "src", "core": "src/config_server/core"},
        include_package_data=True,
        packages=(
            setuptools.find_packages(where="src") +
            setuptools.find_packages(include=('colors*.py',"core")) +
            setuptools.find_packages(where="src/config_server", )
            ),
        classifiers=[
                'Programming Language :: Python :: 3',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                ],
        python_requires='>=3.6',
        install_requires=["pyyaml"],
        )
