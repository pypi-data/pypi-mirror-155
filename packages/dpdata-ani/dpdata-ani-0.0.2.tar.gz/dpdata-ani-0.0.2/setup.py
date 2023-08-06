from setuptools import setup
setup(
    name="dpdata-ani",
    version="0.0.2",
    install_requires = [
        "dpdata >=0.2.7",
        "torchani",
        "torch",
        "numpy",
        "h5py",
    ],
    extras_require = {
        "test": [
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points = {
        'dpdata.plugins': [
            'anidriver=dpdata_ani.anidriver:ANIDriver',
            'ani1xload=dpdata_ani.ani1x:ANI1xFormat',
            'comp6load=dpdata_ani.comp6:COMP6Format',
        ]
    },
    packages = ['dpdata_ani'],
)
