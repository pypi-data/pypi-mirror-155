from setuptools import find_packages, setup
from setuptools.command.build_py import build_py


class _BuildProtos(build_py):

    def run(self):
        import build_protos
        build_protos.rebuild()
        build_py.run(self)


setup(
    name='contek-viper',
    version='3.0',
    description='Viper Python Client',
    url='https://contek.io',
    author='contek_bjy',
    author_email='bjy@contek.io',
    license='private',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: Other/Proprietary License',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['contek_viper'],
    install_requires=[
        'grpcio',
        'protobuf',
    ],
    setup_requires=['grpcio-tools'],
    cmdclass={'build_py': _BuildProtos},
    zip_safe=True,
)
