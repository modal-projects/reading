{
  description = "Agent-native reading spikes site";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            git
            jq
            just
            nodejs_20
            nixfmt-rfc-style
            python312
            uv
          ];

          shellHook = ''
            export UV_PROJECT_ENVIRONMENT=".venv"
            export ASTRO_TELEMETRY_DISABLED=1
            export npm_config_cache="$PWD/.npm-cache"
            echo "reading: nix dev shell ready"
          '';
        };

        formatter = pkgs.nixfmt-rfc-style;
      }
    );
}
