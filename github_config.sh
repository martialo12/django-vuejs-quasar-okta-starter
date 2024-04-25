#!/bin/bash

# Set Git user name
git config --local user.name "martialo12"

# Set Git user email
git config --local user.email "martialo12@yahoo.fr"

# Set Git GPG signing key
git config --local user.signingkey 7C7C9DAC424771EF

# Enable GPG commit signing
git config --local commit.gpgsign true

git config --local --list

echo "Local Git configuration has been updated for this repository."
