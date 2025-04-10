{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    dart2-nixpkgs.url = "github:nixos/nixpkgs?rev=27ae052ce0871efbe6bb0b2d5c60cde313a96ff7";
  };
  outputs =
    { self, ... }@inputs:
    let
      dart2pkgs = inputs.dart2-nixpkgs.legacyPackages.${system};
      python = pkgs.python3;
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      system = "x86_64-linux";

      generateAst = pkgs.writeShellApplication {
        name = "gen-ast";
        runtimeInputs = [ ];
        text = ''
          nix build .#expr-class
          cp result/Expr.py python/Expr.py
          nix build .#stmt-class
          cp result/Stmt.py Stmt.py
          chmod +w python/*.py
        '';
      };
      loxRepl = pkgs.writeShellScriptBin "loxp" ''
        ${python}/bin/python3 ./python
      '';
      loxPythonDevRepl = pkgs.writeShellApplication {
        name = "loxjr";
        runtimeInputs = [ python ];
        text = ''
          python3 "$DEVENV_ROOT/python" "$@"
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
