{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    dart2-nixpkgs.url = "github:nixos/nixpkgs?rev=27ae052ce0871efbe6bb0b2d5c60cde313a96ff7";
  };
  outputs =
    { ... }@inputs:
    let
      dart2pkgs = inputs.dart2-nixpkgs.legacyPackages.${system};
      java = pkgs.jdk23;
      jdt = (pkgs.jdt-language-server.override { jdk = java; });
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      system = "x86_64-linux";
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          dart2pkgs.dart # Dart version 2 is required to build the example Lox
          pkgs.entr
          pkgs.gcc14
          pkgs.gnumake
          pkgs.google-java-format
          pkgs.gradle
          java
          jdt
        ];
        shellHook = ''
          export GRADLE_USER_HOME="$(pwd)/.direnv/state/gradle"
          mkdir -p "$GRADLE_USER_HOME"
        '';
        JDTLS_PATH = "${jdt}/share/java/jdtls/";
      };
    };
}
