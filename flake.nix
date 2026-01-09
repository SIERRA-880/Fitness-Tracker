{
  description = "Django project with Python venv and pip requirements";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python314;
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        name = "django-dev-shell";

        buildInputs = [ python pkgs.git ];

        LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/:${pkgs.zlib}/lib";

        shellHook = ''
          if [ ! -d ".venv" ]; then
            python -m venv .venv
          fi

          source .venv/bin/activate

          if [ -f requirements.txt ]; then
            pip install --upgrade pip
            pip install -r requirements.txt
          else
            echo "[!] No requirements.txt found."
          fi

	  echo "[v] Entered developement environment."
        '';
      };
    };
}
