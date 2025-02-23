[
  {
    name = "Binary";
    fields = [
      {
        type = "Expr";
        name = "left";
      }
      {
        type = "Token";
        name = "operator";
      }
      {
        type = "Expr";
        name = "right";
      }
    ];
  }
  {
    name = "Grouping";
    fields = [
      {
        type = "Expr";
        name = "expression";
      }
    ];
  }
  {
    name = "Literal";
    fields = [
      {
        type = "Object";
        name = "value";
      }
    ];
  }
  {
    name = "Unary";
    fields = [
      {
        type = "Token";
        name = "operator";
      }
      {
        type = "Expr";
        name = "right";
      }
    ];
  }
]
