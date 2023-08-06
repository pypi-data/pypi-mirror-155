from setuptools import find_packages, setup

setup(
    name="contrast-agent-lib",
    version="0.2.0",
    description="Python interface to the contrast agent lib",
    # The project's main homepage.
    url="https://www.contrastsecurity.com",
    project_urls={
        "Support": "https://support.contrastsecurity.com",
    },
    # Author details
    author="Contrast Security, Inc.",
    author_email="python@contrastsecurity.com",
    # Choose your license
    license="CONTRAST SECURITY (see LICENSE.txt)",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # See MANIFEST.in for excluded packages
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"contrast_agent_lib": ["libs/libcontrast_c*"]},
    python_requires=">=3.7",
)
