#! /usr/local/bin/powershell

# This script is used to set up the Python virtual environment and
# install required packages from the poetry.lock file.
# Before executing this script, first install the Python version to be used

# To install dev packages (for library development) run this script as follows:
# ./setup_python_env.ps1 -Dev
# For manual use, the Wait flag can be passed to keep the shell open (useful
# to debug errors during running this script)
# ./setup_python_env.ps1 -Wait

param (
    [switch]$Dev = $false,
    [switch]$Wait = $false
)

Write-Output "Updating pip"
& python -m pip install --upgrade pip

Write-Output "Installing and configuring poetry"
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
& poetry config virtualenvs.in-project true

# Remove the .egg-info to ensure that it is generated properly during package install
$egginfoFolder = "$PSScriptRoot/src/*.egg-info"
if (Test-Path $egginfoFolder) {
    Remove-Item $egginfoFolder -Recurse
}

if ($Dev) {
    Write-Output "Installing project and dev dependencies"
    & poetry install --remove-untracked
    & webdrivermanager firefox
} else {
    Write-Output "Installing project dependencies"
    & poetry install --no-dev --remove-untracked
}

Write-Output "All done!"
if ($Wait) {
    Read-Host "Press <Any> key to close this shell"
}