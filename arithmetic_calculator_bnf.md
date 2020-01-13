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
<Factor> := '(' <Expr> ')' <Expo> | <Variable> <Expo> | [+-] <Factor> <Expo> | number <Expo>
<Expo> := '^'<Factor> <Expo> | e
<Variable> := <AngleF> | <Log> | <Symbol>
<Symbol> := <Expr> | letter
<AngleF> := [sin, cos, tan]'(' <Expr> ')'
<Log> := [log]'('<Expr>')'

곱셈 생략 없음 지원안함
수학상수 sender가 이해 못함 아직
tan^2 이건뭐야
미분 = d()/dx
지수함수 = x^(y+1) 완료
log함수 = log(x) 
-3^2 = 9일지 -9일지 정의
+- |   */  |  -  | ^  | log sin  |  int
```