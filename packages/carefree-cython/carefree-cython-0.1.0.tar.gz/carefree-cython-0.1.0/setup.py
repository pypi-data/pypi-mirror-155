import numpy

from Cython.Build import cythonize
from setuptools import setup
from setuptools import find_packages
from setuptools import Extension


VERSION = "0.1.0"

DESCRIPTION = "Some commonly used cython functions"
with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

INSTALL_REQUIRES = [
    "carefree-toolkit>=0.2.10",
]

setup(
    name="carefree-cython",
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    install_requires=INSTALL_REQUIRES,
    ext_modules=cythonize(
        Extension(
            "cfc.cython_utils",
            sources=["cfc/cython_utils.pyx"],
            language="c",
            include_dirs=[numpy.get_include(), "cfc"],
            library_dirs=[],
            libraries=[],
            extra_compile_args=[],
            extra_link_args=[],
        )
    ),
    package_data={"cfc": ["cython_utils.pyx"]},
    author="carefree0910",
    author_email="syameimaru.saki@gmail.com",
    url="https://github.com/carefree0910/carefree-cython",
    download_url=f"https://github.com/carefree0910/carefree-cython/archive/v{VERSION}.tar.gz",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="python numpy data-science",
)
