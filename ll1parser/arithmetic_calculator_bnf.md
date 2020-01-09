```

Expr := Term ExprTail
ExprTail := [+-] Term ExprTail | e
Term := Factor TermTail
TermTail := [*/] Factor TermTail | e
Factor := '(' Expr ')' | [+-] Factor | number

```
