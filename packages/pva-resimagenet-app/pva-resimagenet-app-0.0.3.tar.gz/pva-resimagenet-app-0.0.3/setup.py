import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pva-resimagenet-app",
    version="0.0.3",
    author="Vadim Pashkin",
    author_email="vaplev@mail.ru",
    description="An application that uses ResImageNet to restore old photos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tailtoon/ResImageNet",
    project_urls={
        "Bug Tracker": "https://github.com/Tailtoon/ResImageNet/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={'pva_resimagenet_app': [r'data/load_icon.gif']},
    include_package_data=True,
    install_requires=[
        'scikit-image',
        'numpy',
        'pyside2',
        'torch',
        'torchvision',
        'torchaudio',
        'torchinfo',
        'pva-resimagenet'
    ],
    python_requires="==3.8.10",
)