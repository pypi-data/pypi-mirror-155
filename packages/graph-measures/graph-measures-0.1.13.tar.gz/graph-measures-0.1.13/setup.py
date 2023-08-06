from setuptools import setup, find_packages
import os
import subprocess

TORCH_VERSION = '1.11.0'
CONDA_PREFIX = os.environ.get("CONDA_PREFIX", None)


def run_makefile():
    # if user use conda run makefile
    if CONDA_PREFIX is not None:
        print("Download version with accelerated calculation.")

        # check if gpu exists
        import torch
        if not torch.cuda.is_available():
            print("Does not support GPU.\nBuild accelerated features.")
            path = os.getcwd() + "/runMakefileCPU.py"
        else:
            print("Support GPU.\nBuild accelerated features for GPU.")
            path = os.getcwd() + "/runMakefileGPU.py"

        # build Makefile
        os.chdir("src/graphMeasures/features_algorithms/accelerated_graph_features/src")
        os.system("conda env create -f env.yml")
        cmd = '. ' + CONDA_PREFIX + '/etc/profile.d/conda.sh && conda activate boost'
        subprocess.call(cmd, shell=True, executable='/bin/bash')
        command = "conda run -n boost python " + path
        process = subprocess.Popen(
            command.split(), stdout=subprocess.PIPE
        )
        output = process.stdout.read()
        print(output)
        output, error = process.communicate()
        print(output)
        print(error)

    else:
        print("Does not use Conda environment or Linux.\nDownload version without accelerated calculation.")


if __name__ == '__main__':
    run_makefile()

    # get text for setup
    with open("requirements.txt") as f:
        requirements = [l.strip() for l in f.readlines()]
        # if CONDA_PREFIX is None:
        #     requirements.append(f"torch~={TORCH_VERSION}")
        # else:
        #     requirements.append(f"pytorch~={TORCH_VERSION}")

    with open("README.md") as r:
        readme = r.read()

    setup(
        name="graph-measures",
        version="0.1.13",
        license="GPL",
        maintainer="Amit Kabya",
        author="Itay Levinas",
        maintainer_email="kabya.amit@gmail.com",
        url="https://github.com/AmitKabya/graph-measures",
        description="A python package for calculating "
                    "topological graph features on cpu/gpu",
        long_description=readme,
        long_description_content_type="text/markdown",
        keywords=["gpu", "graph", "topological-features-calculator"],
        description_file="README.md",
        license_files="LICENSE.rst",
        install_requires=requirements,
        packages=find_packages('src'),
        python_requires=">=3.6.8",
        include_package_data=True,
        package_dir={"": "src"},
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: C++',
            'Operating System :: Unix',
            'Operating System :: POSIX :: Linux',

        ]
    )
