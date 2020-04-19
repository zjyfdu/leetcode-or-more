我在油管上发现一个比较好的[cpp视频](https://www.youtube.com/playlist?list=PLlrATfBNZ98dudnM48yfGUldqGD0S4FFb)

# constructor

```cpp
class Log() {
private:
    Log() {}
public:
    static void Write() {
        // do something
    }
}
```

可以实现不实例化，只能直接用
```cpp
Log::Write(); // ok
Log l;        // not ok
```
也可以这么实现
```cpp
class Log() {

public:
    Log() = delete；
    static void Write() {
        // do something
    }
}
```

# 继承

| 派生方式      | 基类public | 基类protected | 基类private |
| ------------- | ---------- | ------------- | ----------- |
| public派生    | public     | protected     | 不可见      |
| protected派生 | protected  | protected     | 不可见      |
| private派生   | private    | private       | 不可见      |

# [字符串](http://www.cppblog.com/lf426/archive/2010/06/25/118707.html)

编译器的策略也很简单，就是直接读取字符（串）在源文件中的编码数值。
在win32中，wchar_t为16位；linux中是32位。wchar_t同样没有规定编码
```cpp
const wchar_t* ws = L"中文abc";
```
的编码分别为：
```cpp
0x4E2D   0x6587    0x0061   0x0062   0x0063                            //win32，16位
0x00004E2D   0x00006587    0x00000061   0x00000062   0x00000063        //linux，32位
```
大写的L是告诉编译器：这是宽字符串。所以，这时候是需要编译器根据locale（本地化策略集）来进行翻译的。
