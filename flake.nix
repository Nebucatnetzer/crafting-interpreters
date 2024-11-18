{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };
  outputs =
    { ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      jdt = (pkgs.jdt-language-server.override { jdk = pkgs.jdk21; });
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.google-java-format
          pkgs.gradle
          pkgs.jdk21
          jdt
        ];
        JDTLS_PATH = "${jdt}/share/java/jdtls/";
      };
    };
}
