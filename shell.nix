# This allows overriding pkgs by passing `--arg pkgs ...`
{ pkgs ? import <nixpkgs> {}, pinned ? null }:
let
  project = import ./default.nix 
      { inherit pinned; } //
      (if (isNull pinned) then { inherit pkgs; } else {});
in with project.pkgs;

mkShell {
  buildInputs = [
    # put packages here.
    project.python
  ];

  shellHook = ''
  '';
}
