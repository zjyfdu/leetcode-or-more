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

# cpp的特征

封装、继承、多态

# 构造函数
 
[拷贝构造函数和赋值](https://www.cnblogs.com/wangguchangqing/p/6141743.html)

```
String(const String& other);
String& String::operator =(const String& other)
```

友元函数

```
class complex {
    private:
       double re;
       double im;
    public:
       complex(double real = 0.0, double imag = 0.0) : re(real), im(imag) {}
       friend ostream & operator<<(ostream& os, complex& c);
};

ostream & operator<<(ostream& os, complex& c){
    os << c.re << std::showpos << c.im;
    return os;
}
```

# 单例模式

我感觉c++应该不会问这个，参考[这个](https://www.youtube.com/watch?v=PPup1yeU45I)视频吧

直接用namespace就可以

# explicit（显式）关键字

# 矩阵乘

## 头文件 matrix.h

```
#ifndef __MATRIX_H
#define __MATRIX_H

#include <vector>

template <class T>
class Matrix {
private:
    std::vector<std::vector<T> > mat;
    unsigned rows;
    unsigned cols;

public:
    Matrix(unsigned _rows, unsigned _cols, const T& _initial);
    Matrix(const Matrix<T>& rhs);
    virtual ~Matrix();

    // Operator overloading, for "standard" mathematical matrix operations
    Matrix<T>& operator=(const Matrix<T>& rhs);

    // Matrix mathematical operations
    Matrix<T> operator*(const Matrix<T>& rhs);
    Matrix<T>& operator*=(const Matrix<T>& rhs);

    // Access the individual elements
    T& operator()(const unsigned& row, const unsigned& col);
    const T& operator()(const unsigned& row, const unsigned& col) const;

    // Access the row and column sizes
    unsigned get_rows() const;
    unsigned get_cols() const;

};

#endif
```

## matrix.cpp

```
#include "matrix.h"

// Parameter Constructor                                                                                                                                                      
template<class T>
Matrix<T>::Matrix(unsigned _rows, unsigned _cols, const T& _initial) {
  mat.resize(_rows);
  for (unsigned i=0; i<mat.size(); i++) {
    mat[i].resize(_cols, _initial);
  }
  rows = _rows;
  cols = _cols;
}

// Copy Constructor                                                                                                                                                           
template<class T>
Matrix<T>::Matrix(const Matrix<T>& rhs) {
  mat = rhs.mat;
  rows = rhs.get_rows();
  cols = rhs.get_cols();
}

// (Virtual) Destructor                                                                                                                                                       
template<class T>
Matrix<T>::~Matrix() {}

// Assignment Operator                                                                                                                                                        
template<class T>
Matrix<T>& Matrix<T>::operator=(const Matrix<T>& rhs) {
  if (&rhs == this)
    return *this;

  unsigned new_rows = rhs.get_rows();
  unsigned new_cols = rhs.get_cols();

  mat.resize(new_rows);
  for (unsigned i=0; i<mat.size(); i++) {
    mat[i].resize(new_cols);
  }

  for (unsigned i=0; i<new_rows; i++) {
    for (unsigned j=0; j<new_cols; j++) {
      mat[i][j] = rhs(i, j);
    }
  }
  rows = new_rows;
  cols = new_cols;

  return *this;
}

// Left multiplication of this matrix and another                                                                                                                              
template<class T>
Matrix<T> Matrix<T>::operator*(const Matrix<T>& rhs) {
  unsigned rows = this->get_rows();
  unsigned cols = rhs.get_cols();
  Matrix result(rows, cols, 0.0);

  for (unsigned i=0; i<rows; i++) {
    for (unsigned j=0; j<cols; j++) {
      for (unsigned k=0; k<this->get_cols(); k++) {
        result(i,j) += this->mat[i][k] * rhs(k,j);
      }
    }
  }

  return result;
}

// Cumulative left multiplication of this matrix and another                                                                                                                  
template<class T>
Matrix<T>& Matrix<T>::operator*=(const Matrix<T>& rhs) {
  Matrix result = (*this) * rhs;
  (*this) = result;
  return *this;
}

// Access the individual elements                                                                                                                                             
template<class T>
T& Matrix<T>::operator()(const unsigned& row, const unsigned& col) {
  return this->mat[row][col];
}

// Access the individual elements (const)                                                                                                                                     
template<class T>
const T& Matrix<T>::operator()(const unsigned& row, const unsigned& col) const {
  return this->mat[row][col];
}

// Get the number of rows of the matrix                                                                                                                                       
template<class T>
unsigned Matrix<T>::get_rows() const {
  return this->rows;
}

// Get the number of columns of the matrix                                                                                                                                    
template<class T>
unsigned Matrix<T>::get_cols() const {
  return this->cols;
}

template <class T>
ostream & operator<<(ostream &out, Matrix<T> &a)
{
    for (unsigned i = 0; i < a.get_row(); i++) {
        for (unsigned j = 0; j < a.get_col(); j++) {
            out << a(i, j) << "\t";
        }
        out << std::endl;
    }
    return out;
}

// 实例化声明
template class Matrix<int>;
template class Matrix<float>;
template class Matrix<double>;

```