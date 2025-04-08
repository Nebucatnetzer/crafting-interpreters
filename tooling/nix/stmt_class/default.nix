{
  google-java-format,
  lib,
  stdenvNoCC,
}:
let
  statements = import ./statements.nix;

  # Function to generate the Visitor interface methods
  genVisitorMethods =
    classes:
    lib.concatMapStringsSep "\n    " (class: "R visit${class.name}Stmt(${class.name} stmt);") classes;

  # Function to generate the constructor for a class
  genConstructor =
    class:
    let
      params = lib.concatStringsSep ", " (map (field: "${field.type} ${field.name}") class.fields);
      assignments = lib.concatStringsSep "\n      " (
        map (field: "this.${field.name} = ${field.name};") class.fields
      );
    in
    ''
      ${class.name}(${params}) {
        ${assignments}
      }
    '';

  # Function to generate the fields for a class
  genFields =
    fields: lib.concatMapStringsSep "\n    " (field: "final ${field.type} ${field.name};") fields;

  # Function to generate each class
  genClasses =
    classes:
    lib.concatMapStringsSep "\n\n  " (class: ''
      static class ${class.name} extends Stmt {
        ${genConstructor class}

        @Override
        <R> R accept(Visitor<R> visitor) {
          return visitor.visit${class.name}Stmt(this);
        }

        ${genFields class.fields}
      }
    '') classes;

  javaTemplate = ''
    package org.zweili.lox;

    abstract class Stmt {
      interface Visitor<R> {
        ${genVisitorMethods statements}
      }

      ${genClasses statements}

      abstract <R> R accept(Visitor<R> visitor);
    }
  '';
in
stdenvNoCC.mkDerivation {
  name = "lox-stmt-class";
  dontBuild = true;
  unpackPhase = "true";
  buildInputs = [
    google-java-format
  ];

  installPhase = ''
    mkdir -p $out
    echo "${javaTemplate}" > $out/Stmt.java
    google-java-format --replace $out/Stmt.java
  '';
}
