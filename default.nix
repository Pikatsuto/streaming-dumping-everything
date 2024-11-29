# save this as shell.nix
{ pkgs ? import <nixpkgs> { config.allowUnfree = true; }}:

pkgs.mkShell {
  packages = with pkgs; [
    python312Full
    python312Packages.setuptools
    python312Packages.flake8
    python312Packages.wheel
    chromedriver
    chromium
    gnumake
  ];
}