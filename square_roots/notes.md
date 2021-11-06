# Computing square roots
By only using addition and multiplication

## Initial experiment: flawed math
My initial idea was as follows:

**`ComputePower(n := num digits, k := number to compute k^¼ of)`**
```python
cumsum := 0
d := [None]*n #empty array of length n

for i = 0 to n:
    choose d[i] as an integer in [0, 9] 
        such that cumsum*(1 + 0.1**i * d[i])**2 <= k
    cumsum += (0.1**i * d[i])**2
return f"{d[0]}.{d[1]}{d[2]}etc..."
```

This approach does not work, as it ignores binomial expansion. 
That is, the term `(1 + 0.1**i * d[i])**2` is only multiplied with `cumsum`.
and not with the digits that will be added later.

## Second approach: brute force
Silimar to the above, but now check if `(cumsum + 0.1**i * d[i]) <= k`;
the square of cumsum is recompute every iteration.