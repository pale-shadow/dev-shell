# shell

## Single User Nix Shell install

To install Nix from any Linux distribution, use the following two commands.
(Note: This assumes you have the permission to use sudo, and you are logged
in as the user you want to install Nix for.)

```sh
sudo install -d -m755 -o $(id -u) -g $(id -g) /nix
curl -L https://nixos.org/nix/install | sh

Then don't forget to run the command provided at the end of the installation
script to make nix available in your system:

* BASH users (you probably want this)

```sh
source $HOME/.nix-profile/etc/profile.d/nix.sh
```

* For FISH users (you can probably skip this)

```sh
set -x NIX_PATH (echo $NIX_PATH:)nixpkgs=$HOME/.nix-defexpr/channels/nixpkgs
```

Now you can use the virtual envrionment:

```sh
nix-shell
python -m pip install -rrequirements.txt
python3 -m gaming_migration
exit
nix-collect-garbage -d
```

