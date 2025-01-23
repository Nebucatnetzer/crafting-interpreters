{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };
  outputs =
    { ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      java = pkgs.jdk23;
      jdt = (pkgs.jdt-language-server.override { jdk = java; });
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.google-java-format
          pkgs.gradle
          java
          jdt
        ];
        JDTLS_PATH = "${jdt}/share/java/jdtls/";
      };
    };
}
