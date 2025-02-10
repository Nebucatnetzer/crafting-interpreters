{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    dart2-nixpkgs.url = "github:nixos/nixpkgs?rev=27ae052ce0871efbe6bb0b2d5c60cde313a96ff7";
  };
  outputs =
    { self, ... }@inputs:
    let
      DEVENV_ROOT = builtins.getEnv "PWD";
      dart2pkgs = inputs.dart2-nixpkgs.legacyPackages.${system};
      java = pkgs.jdk23_headless;
      jdt = (pkgs.jdt-language-server.override { jdk = java; });
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      system = "x86_64-linux";
      loxRepl = pkgs.writeShellApplication {
        name = "loxjr";
        runtimeInputs = [ java ];
        text = ''
          java ${self}/java/org/zweili/Lox.java "$@"
        '';
      };
      loxJavaDevRepl = pkgs.writeShellApplication {
        name = "loxjr";
        runtimeInputs = [ java ];
        text = ''
          java "${DEVENV_ROOT}/java/org/zweili/Lox.java" "$@"
        '';
      };
    in
    {

      packages.${system} = {
        lox-repl = loxRepl;
        default = self.packages.${system}.lox-repl;
      };
      devShells.${system}.default = pkgs.mkShell {
        inherit DEVENV_ROOT;
        buildInputs = [
          dart2pkgs.dart # Dart version 2 is required to build the example Lox
          java
          jdt
          loxJavaDevRepl
          pkgs.entr
          pkgs.gcc14
          pkgs.gnumake
          pkgs.google-java-format
        ];
        JDTLS_PATH = "${jdt}/share/java/jdtls/";
      };
    };
}
