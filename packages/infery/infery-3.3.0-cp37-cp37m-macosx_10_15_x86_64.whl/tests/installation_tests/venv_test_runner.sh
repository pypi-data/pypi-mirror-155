#! /bin/bash

set -e -x

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

function die {
    echo "ERROR: $2"
    exit $1
}

# REQUIRED ARGS
venv_dir=0
requirements_path=0

arg_help=0
arg_gpu_present=0
arg_dont_install_infery=0
arg_reinstall_requirements=0

while [[ "$#" -gt 0 ]]; do case $1 in
  --venv-dir) venv_dir="$2"; shift;;
  --requirements-path) requirements_path="$2"; shift;;
  --gpu-present) arg_gpu_present=1;;
  --dont-install-infery) arg_dont_install_infery=1;;
  --reinstall-requirements) arg_reinstall_requirements=1;;
  -h|--help) arg_help=1;;
  *) echo "Unknown parameter passed: $1"; echo "For help type: $0 --help"; exit 1;
esac; shift; done

if [[ "$arg_help" -eq "1" || "$venv_dir" -eq "0" || "$requirements_path" -eq "0" ]]; then
    echo "Usage: $0"
    echo "    --venv-dir <venv_dir>"
    echo "    --requirements-path <requirements_path>"
    echo "    [--gpu-present]"
    echo "    [--dont-install-infery]"
    echo "    [--reinstall-requirements]"
    exit 1
fi

source "$venv_dir/bin/activate" || die 2 "failed to source into venv"

pip install --upgrade pip

pip install                                                                     \
    --extra-index-url https://pypi.ngc.nvidia.com                               \
    -r "$SCRIPT_DIR/$requirements_path"                                         \
    || die 3 "failed to install requirements"

if [[ "$arg_dont_install_infery" -eq "0" ]]; then
    if [[ "$arg_gpu_present" -eq "1" ]]; then
        pip install --extra-index-url https://pypi.ngc.nvidia.com infery-gpu    \
            || die 4 "failed to install infery-gpu"
    else
        pip install infery || die 4 "failed to install infery"
    fi
fi

if [[ "$arg_reinstall_requirements" -eq "1" ]]; then
    pip install                                                                 \
        --extra-index-url https://pypi.ngc.nvidia.com                           \
        -r "$SCRIPT_DIR/$requirements_path"                                     \
        || die 5 "failed to re-install requirements after infery installation"
fi

python "$SCRIPT_DIR/run_tests_in_venv.py" || die 100 "tests failed in venv"
