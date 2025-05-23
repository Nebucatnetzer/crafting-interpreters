{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    dart2-nixpkgs.url = "github:nixos/nixpkgs?rev=27ae052ce0871efbe6bb0b2d5c60cde313a96ff7";
  };
  outputs =
    { self, ... }@inputs:
    let
      dart2pkgs = inputs.dart2-nixpkgs.legacyPackages.${system};
      java = pkgs.jdk23_headless;
      jdt = (pkgs.jdt-language-server.override { jdk = java; });
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      system = "x86_64-linux";

      generateAst = pkgs.writeShellApplication {
        name = "gen-ast";
        runtimeInputs = [ ];
        text = ''
          nix build .#expr-class
          cp result/Expr.java java/org/zweili/lox/Expr.java
          nix build .#stmt-class
          cp result/Stmt.java java/org/zweili/lox/Stmt.java
          chmod +w java/org/zweili/lox/*.java
        '';
      };
      loxRepl = pkgs.stdenvNoCC.mkDerivation {
        name = "loxjr";
        src = self;
        nativeBuildInputs = [ pkgs.makeWrapper ];
        buildInputs = [ java ];
        buildPhase = ''
          runHook preBuild

          mkdir -p out/
          javac -d out/ -sourcepath java/ -classpath out/ -encoding utf8 java/org/zweili/lox/*.java

          runHook postBuild
        '';

        installPhase = ''
          runHook preInstall

          mkdir -p $out/lib/
          mv out $out/lib/lox

          makeWrapper ${java}/bin/java $out/bin/loxjr \
            --add-flags "-classpath $out/lib/lox org.zweili.lox.Lox"

          runHook postInstall
        '';
      };
      loxJavaDevRepl = pkgs.writeShellApplication {
        name = "loxjr";
        runtimeInputs = [ java ];
        text = ''
          java "$DEVENV_ROOT/java/org/zweili/lox/Lox.java" "$@"
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
          java
          jdt
          loxJavaDevRepl
          pkgs.entr
          pkgs.gcc14
          pkgs.gnumake
          pkgs.google-java-format
        ];
        shellHook = ''
          DEVENV_ROOT="$PWD"
          export DEVENV_ROOT
          ln -snf  "${java}"/lib/openjdk "$DEVENV_ROOT"/.direnv/java;
        '';
        JDTLS_PATH = "${jdt}/share/java/jdtls/";
      };
    };
}
