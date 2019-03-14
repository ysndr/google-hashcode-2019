let
  # Look here for information about how to generate `nixpkgs-version.json`.
  #  → https://nixos.wiki/wiki/FAQ/Pinning_Nixpkgs
  pinnedVersion = pin: builtins.fromJSON (builtins.readFile pin);
  pinnedPkgs = pin:  import (builtins.fetchTarball {
    inherit (pinnedVersion pin) url sha256;
  }) {};
  pkgs' = pinned: (
    if (!isNull pinned) then pinnedPkgs pinned 
    else import <nixpkgs> {});

  hies-pkgs = import (builtins.fetchTarball {
    url = "https://github.com/domenkozar/hie-nix/tarball/master";
  });
in
{ pkgs ? pkgs' pinned, pinned ? null, enable-hie ? false }:
with  import pkgs.path { 
  overlays = [ 
    (self: super: {
      enchant = super.enchant.overrideAttrs (oldAttrs: rec {
        postConfigure = ''
        substituteInPlace src/Makefile --replace \
         '$(AM_V_lt) $(AM_LIBTOOLFLAGS)'\
         '$(AM_V_lt) --tag=CC $(AM_LIBTOOLFLAGS)'
        '';
      }); 
    })];
  };
let
  # ------------- Python ----------------
  # for build usage only

  python' = python3.override {  
    packageOverrides = self: super: {
      pylint = super.pylint.overridePythonAttrs(old: rec {
        doCheck = false;  
      });
    };
  };

  python-env = python'.withPackages(pp: with pp; [
      ipython
      pip
      virtualenv
      pylint
      autopep8
  ]);
  # --------------- Commands ----------------


in {
  #inherit (pkgs)  libyaml libiconv;
  python-env = python-env;
} 
