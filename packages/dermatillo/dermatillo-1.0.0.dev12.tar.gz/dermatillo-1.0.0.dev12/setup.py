import os
import dermatillo
import setuptools
import subprocess
from pybind11.setup_helpers import Pybind11Extension

script_dir = os.path.dirname(os.path.realpath(__file__))


def get_arch():
    return subprocess.check_output(["uname", "-m"]).decode("ascii").replace("\n", "")


def load_requirements(file_name):
    with open(os.path.join(script_dir, "requirements", file_name)) as f:
        requirements = f.readlines()
    return [req.replace("\n", "") for req in requirements]


if __name__ == "__main__":
    name = "dermatillo"
    version = dermatillo.__version__
    description = dermatillo.__doc__

    author = "Jan Grzybek"
    author_email = "lyre_embassy_0n@icloud.com"

    entry_points = {
        "console_scripts": [
            "dermatillo = dermatillo.cli:entry"
        ]
    }

    python_requires = '>=3.9'
    install_requires = load_requirements("dermatillo.txt")

    packages = [
        "dermatillo"
    ]

    project_urls = {
        "GitHub": "https://github.com/jan-grzybek/dermatillo"
    }

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ]

    os.environ["ARCHFLAGS"] = f"-arch {get_arch()}"
    ext_modules = [
        Pybind11Extension("dermatillo_pp",
                          ["dataset/pre_processing/pre_processor.cpp"],
                          define_macros=[("VERSION_INFO", version)],
                          extra_compile_args=["-std=c++17"])
    ]

    subprocess.run(["cp", os.path.join(script_dir, "LICENSE"), os.path.join(script_dir, "dermatillo/files/")])

    setuptools.setup(
        name=name,
        version=version,
        author=author,
        author_email=author_email,
        description=description,
        entry_points=entry_points,
        license="MIT",
        install_requires=install_requires,
        python_requires=python_requires,
        packages=packages,
        ext_modules=ext_modules,
        classifiers=classifiers,
        include_package_data=True,
        project_urls=project_urls,
    )
