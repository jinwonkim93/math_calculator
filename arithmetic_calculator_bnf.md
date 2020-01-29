```

Expr := Term ExprTail
ExprTail := [+-] Term ExprTail | e
Term := Factor TermTail
TermTail := [*/] Factor TermTail | e
Factor := '(' Expr ')' | [+-] Factor | number

```


```
위에서 derivative 일지 아닐지 
<Expr> := <Term> <ExprTail>
<ExprTail> := [+-] <Term> <ExprTail> | e
<Term> := <Factor> <TermTail>
<TermTail> := [*/] <Factor> <TermTail> | e
<Factor> := '(' <Expr> ')' <Expo> | <Variable> <Expo> | [+-] <Factor> <Expo> | Constant <Expo>
<Expo> := '^'<Factor> <Expo> | e
<Variable> := <AngleF> | <Log> | <specialNum> | <Symbol>
<Special> := e | pi
<Symbol> := <Expr> | letter
<AngleF> := [sin, cos, tan]'(' <Expr> ')'
<Log> := [log]'('<Expr>')'

그림 그리기
점 갯수 한정
plot 위치 지정
+- |   */  |  -  | ^  | log sin  |  int
````