{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    dart2-nixpkgs.url = "github:nixos/nixpkgs?rev=27ae052ce0871efbe6bb0b2d5c60cde313a96ff7";
  };
  outputs =
    { self, ... }@inputs:
    let
      dart2pkgs = inputs.dart2-nixpkgs.legacyPackages.${system};
      gradle = pkgs.gradle.override {
        java = java;
      };
      java = pkgs.jdk23;
      jdt = (pkgs.jdt-language-server.override { jdk = java; });
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      system = "x86_64-linux";
      loxRepl = pkgs.writeShellApplication {
        name = "loxr";
        runtimeInputs = [ java ];
        text = ''
          java ${self}/java/src/main/java/org/zweili/Lox.java "$@"
        '';
      };
    in
    {

      packages.${system} = {
        lox-repl = loxRepl;
      };
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          dart2pkgs.dart # Dart version 2 is required to build the example Lox
          gradle
          java
          jdt
          pkgs.entr
          pkgs.gcc14
          pkgs.gnumake
          pkgs.google-java-format
        ];
        shellHook = ''
          export GRADLE_USER_HOME="$(pwd)/.direnv/state/gradle"
          mkdir -p "$GRADLE_USER_HOME"
        '';
        JDTLS_PATH = "${jdt}/share/java/jdtls/";
      };
    };
}
