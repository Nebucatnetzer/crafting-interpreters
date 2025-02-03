# crafting-interpreters

https://craftinginterpreters.com/contents.html

## Development Setup

Make sure you have Nix and direnv installed.

1. Enter directory and run `direnv allow`.
2. After Nix is finished run `gradle` it does some stuff.

To run the application simply run: `java ./java/src/main/java/org/zweili/Lox.java`

## Running LoxRepl

```
nix run .#lox-repl
```
