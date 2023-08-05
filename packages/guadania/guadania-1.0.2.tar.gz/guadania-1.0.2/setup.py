import setuptools

DESC = 'Libreria que matará vuestro sufrimiento por la PARCA'

setuptools.setup(
    name='guadania',
    description=DESC,
    version='1.0.2',
    packages=[
        'guadania',
        'guadania.prisma'
    ],
    python_requires='>=3.7'
)