def fun(n):
    a0=10000
    if(n!=0):
        a0=fun(n-1)*1.1
    return a0
n=int(input(":"))
val=int(fun(n))
print(val)
#val=int(val/500)
i=0
while i<n:
    v=int(fun(i)/500)
    j=0
    while j<v:
        print("#",end="")
        j+=1
    print()
    i+=1