package org.zweili;

// TODO: Apperently static imports are considered to bad style. What would be
// the good style? I prefer to be explicit.
import static org.zweili.TokenType.*;

import java.util.ArrayList;
import java.util.List;

class Scanner {
  private final String source;
  private final List<Token> tokens = new ArrayList<>();
  private int start = 0;
  private int current = 0;
  private int line = 1;

  Scanner(String source) {
    this.source = source;
  }

  List<Token> scanTokens() {
    while (!isAtEnd()) {
      // We are at the beginning of the next lexeme.
      this.start = this.current;
      scanToken();
    }
    this.tokens.add(new Token(TokenType.EOF, "", null, line));
    return this.tokens;
  }

  private void scanToken() {
    char c = advance();
    switch (c) {
      case '(':
        addToken(LEFT_PAREN);
        break;
      case ')':
        addToken(RIGHT_PAREN);
        break;
      case '{':
        addToken(LEFT_BRACE);
        break;
      case '}':
        addToken(RIGHT_BRACE);
        break;
      case ',':
        addToken(COMMA);
        break;
      case '.':
        addToken(DOT);
        break;
      case '-':
        addToken(MINUS);
        break;
      case '+':
        addToken(PLUS);
        break;
      case ';':
        addToken(SEMICOLON);
        break;
      case '*':
        addToken(STAR);
        break;
    }
  }

  private boolean isAtEnd() {
    return this.current >= this.source.length();
  }

  private char advance() {
    return this.source.charAt(this.current++);
  }

  private void addToken(TokenType type) {
    addToken(type, null);
  }

  private void addToken(TokenType type, Object literal) {
    String text = this.source.substring(start, current);
    this.tokens.add(new Token(type, text, literal, line));
  }
}
