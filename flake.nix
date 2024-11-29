{
  description = "streaming-dumping-everything";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in with pkgs; rec {
        # Development environment
        devShell = mkShell {
          name = "flask-example";
          nativeBuildInputs = [ python3 poetry ];
        };

        # Runtime package
        packages.streaming-dumping-everything = callPackage ./package.nix {};

        # The default package when a specific package name isn't specified.
        defaultPackage = packages.streaming-dumping-everything;
      }
    );
}

