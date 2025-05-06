[
  {
    name = "Block";
    fields = [
      {
        type = "list[Stmt]";
        name = "statements";
      }
    ];
  }
  {
    name = "Expression";
    fields = [
      {
        type = "Expr";
        name = "expression";
      }
    ];
  }
  {
    name = "Print";
    fields = [
      {
        type = "Expr";
        name = "expression";
      }
    ];
  }
  {
    name = "Var";
    fields = [
      {
        type = "Token";
        name = "name";
      }
      {
        type = "Expr";
        name = "initializer";
      }
    ];
  }
]
