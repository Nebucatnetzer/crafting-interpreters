{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    dart2-nixpkgs.url = "github:nixos/nixpkgs?rev=27ae052ce0871efbe6bb0b2d5c60cde313a96ff7";
  };
  outputs =
    { self, ... }@inputs:
    let
      pyproject = pkgs.lib.importTOML ./pyproject.toml;
      myPython = pkgs.python312.override {
        self = myPython;
        packageOverrides = pyfinal: pyprev: {
          # An editable package with a script that loads our mutable location
          lox-editable = pyfinal.mkPythonEditablePackage {
            # Inherit project metadata from pyproject.toml
            pname = pyproject.project.name;
            inherit (pyproject.project) version;

            # The editable root passed as a string
            root = "$DEVENV_ROOT/python/lox"; # Use environment variable expansion at runtime

            inherit (pyproject.project) ;
          };
        };
      };

      dart2pkgs = inputs.dart2-nixpkgs.legacyPackages.${system};
      python = myPython.withPackages (p: [
        p.black
        p.isort
        p.lox-editable
        p.mypy
        p.pylint
        p.pylsp-mypy
        p.pytest
        p.python-lsp-ruff
        p.python-lsp-server
        p.ruff
      ]);
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      system = "x86_64-linux";

      generateAst = pkgs.writeShellApplication {
        name = "gen-ast";
        runtimeInputs = [ ];
        text = ''
          nix build .#expr-class
          cp result/Expr.py python/lox/Expr.py
          nix build .#stmt-class
          cp result/Stmt.py python/lox/Stmt.py
          chmod +w python/*.py
        '';
      };
      loxRepl = pkgs.writeShellScriptBin "loxp" ''
        ${python}/bin/python3 ./python/lox
      '';
      loxPythonDevRepl = pkgs.writeShellApplication {
        name = "loxp";
        runtimeInputs = [ python ];
        text = ''
          python3 "$DEVENV_ROOT/python/lox" "$@"
        '';
      };
    in
    {
      packages.${system} = {
        expr-class = pkgs.callPackage ./tooling/nix/expr_class { };
        lox-repl = loxRepl;
        stmt-class = pkgs.callPackage ./tooling/nix/stmt_class { };
        default = self.packages.${system}.lox-repl;
      };
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          dart2pkgs.dart # Dart version 2 is required to build the example Lox
          generateAst
          loxPythonDevRepl
          python
          pkgs.entr
          pkgs.gcc14
          pkgs.gnumake
        ];
        shellHook = ''
          DEVENV_ROOT="$PWD"
          export DEVENV_ROOT
        '';
      };
    };
}
