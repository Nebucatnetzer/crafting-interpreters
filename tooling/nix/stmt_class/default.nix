{
  black,
  lib,
  stdenvNoCC,
}:
let
  statements = import ./statements.nix;

  # Function to generate the constructor for a class
  genConstructor =
    class:
    let
      params = lib.concatStringsSep ", " (map (field: "${field.name}: ${field.type}") class.fields);
      assignments = lib.concatStringsSep "\n    " (
        map (field: "    self.${field.name} = ${field.name}") class.fields
      );
    in
    ''
      def __init__(self, ${params}) -> None:
          ${assignments}
    '';

  # Function to generate each class
  genClasses =
    classes:
    lib.concatMapStringsSep "\n\n" (class: ''
      class ${class.name}(Stmt):
          ${genConstructor class}
          def accept(self, visitor):
              return visitor.visit_${lib.toLower class.name}_stmt(self);

    '') classes;

  pythonTemplate = ''
    from abc import ABC
    from abc import abstractmethod

    from expressions import Expr
    from token_cls import Token
    from visitor import Visitor

    class Stmt(ABC):
        @abstractmethod
        def accept(self, visitor: Visitor):
            pass

    ${genClasses statements}
  '';
in
stdenvNoCC.mkDerivation {
  name = "lox-stmt-class";
  dontBuild = true;
  unpackPhase = "true";
  buildInputs = [
    black
  ];

  installPhase = ''
    mkdir -p $out
    echo "${pythonTemplate}" > $out/stmt.py
    black $out/stmt.py
  '';
}
