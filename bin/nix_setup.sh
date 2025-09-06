#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2023-2025 franklin <smoooth.y62wj@passmail.net>
#
# SPDX-License-Identifier: MIT

function check_if_root() {
  if [[ $(id -u) -ne 0 ]]; then echo -e "${RED}Only run his script as root.${NC}" && exit 1; fi
  # check if user can sudo
  # sudo -l -U `whoami` | grep -i nopasswd
}

function install() {
  yes | sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon
  nix-shell -p nix-info --run "nix-info -m"
  echo "you need to close this shell and log in again"
}

function uninstall() {
  # i stole these commands from https://nix.dev/manual/nix/2.30/installation/uninstall.html

  # Remove the Nix daemon service
  systemctl stop nix-daemon.service
  systemctl disable nix-daemon.socket nix-daemon.service
  systemctl daemon-reload

  # Remove files created by Nix:
  rm -rf /etc/nix /etc/profile.d/nix.sh /etc/tmpfiles.d/nix-daemon.conf /nix ~root/.nix-cha

  # Remove build users and their group
  for i in $(seq 1 32); do
    userdel nixbld$i
  done
  groupdel nixbld

  # There may also be references to Nix in
  # NIX_REF=( /etc/bash.bashrc /etc/bashrc /etc/profile /etc/zsh/zshrc /etc/zshrc )
  # you can loop over it here and grep out the detritus
}

function main() {
  check_if_root
  # install
  uninstall
}

main "$@"
