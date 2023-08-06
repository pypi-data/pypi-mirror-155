from setuptools import find_packages, setup

with open(r"README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="do_random",
    version="0.0.4",
    description="random and random",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/HowieHz/do_random",
    author="HowieHz",
    python_requires='>=3.7',
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[],
    project_urls={
        "Bug Reports": "https://github.com/HowieHz/do_random/issues",
    },
)
