# 从1加到100


```
sum=0
for (( i=1; i<=100; i++ ))
do
    ((sum=sum+i))
done
echo $sum
```

```
let sum=0
for i in {1..100}
do
    let sum=sum+i
done
echo $sum
```