import setuptools

long_description = ""

setuptools.setup(
    name="EAyd_veriOnisleme",
    version="0.0.2",
    author="Emrah Aydemir",
    author_email="aydemir.emrah23@gmail.com",
    description="Veri önişleme aşamalarında sık kullanılan metotlar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.5',
    install_requires=["numpy","keras"]
)