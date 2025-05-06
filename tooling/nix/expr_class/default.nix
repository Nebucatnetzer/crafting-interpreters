{
  black,
  lib,
  stdenvNoCC,
}:
let
  expressions = import ./expressions.nix;

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
      class ${class.name}(Expr):
          ${genConstructor class}
          def accept(self, visitor):
              return visitor.visit_${lib.toLower class.name}_expr(self)

    '') classes;

  pythonTemplate = ''
    from abc import ABC
    from abc import abstractmethod

    from lox.token_cls import Token

    class Expr(ABC):
      @abstractmethod
      def accept(self, visitor):
          pass


    ${genClasses expressions}
  '';
in
stdenvNoCC.mkDerivation {
  name = "lox-expr-class";
  dontBuild = true;
  unpackPhase = "true";
  buildInputs = [
    black
  ];

  installPhase = ''
    mkdir -p $out
    echo "${pythonTemplate}" > $out/expr.py
    black $out/expr.py
  '';
}
