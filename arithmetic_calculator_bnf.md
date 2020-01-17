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
<Variable> := <AngleF> | <Log> | <Symbol>
<Symbol> := <Expr> | letter
<AngleF> := [sin, cos, tan]'(' <Expr> ')'
<Log> := [log]'('<Expr>')'

현재 안되는거
삼각함수 - has no attribute symbol
로그 - has no attribute symgbol
삼각함수 - 제곱 안됌
정의역 치역
1/x 가 안되고 있었음 ㄷㄷ
+- |   */  |  -  | ^  | log sin  |  int
````