# 第一章

- [字符串到整数（atoi）](https://leetcode-cn.com/problems/string-to-integer-atoi/)
  - 需要注意一些特殊情况，像+、-、INT_MIN、INT_MAX、等细节
  - 应该不会出现在电话面试里，白板倒是挺有可能
  - 如果是指针的话，第一把先判断空指针

```cpp
class Solution {
public:
    int myAtoi(string str) {
        long res = 0;
        int index = 0;
        bool is_postive = true;
        while(index < str.size() && str[index] == ' ') {
            index++;
        }
        if (index < str.size() && str[index] == '-') {
            is_postive = false;
            index++;
        } else if (index < str.size() && str[index] == '+') {
            is_postive = true;
            index++;
        }
        while(index < str.size() && str[index] >= '0' && str[index] <= '9') {
            res = res * 10 + str[index] - '0';
            index++;
            if (is_postive && res >= INT_MAX) {
                return INT_MAX;
            } else if (!is_postive && -1 * res <= INT_MIN) {
                return INT_MIN;
            }
        }
        return is_postive ? res : -1 * res;
    }
};
```

- 复制构造函数不可以传值

```cpp
class A
{
private:
    int value;

public:
    A(int n) { value = n; }
    A(A other) { value = other.value; } 
    // 编译错误，形参复制到实参也会调用复制构造函数，形成递归调用，最后栈溢出。
    // 应该用 A(const A& other) { value = other.value; }

};
```

- 赋值运算符函数
  - 还可以有异常安全的更高级写法，这里没有写

```cpp
class CMyString
{
public:
    CMyString(char* pData = NULL);
    CMyString(const CMyString& str);
    ~CMyString(void);

private:
    char* m_pData;
}
```


```cpp
CMyString& CMyString::operator = (const CMystring &str) {
    if (this == &str)
    // 返回*this，是为了可以连等str1=str2=str3，等号是从右到左的
        return *this;
    
    delete []m_pData;
    m_pData = new char(strlen(str.m_pData) + 1);
    strcpy(m_Pdata, str.m_pData);
    return *this;
}
```

- 二维数组中的查找
  - 二维数组每一行和每一列都是递增排列的，需要搜索某一个数是否在二维数组中存在
  - 诀窍是从右上角开始
  - 这个题目没有在leetcode上找到，直接干写吧

```cpp
bool findPartiialSortedArray(vector<vector<int> > &arr, int num) {
    int rows = arr.length();
    int columns = arr[0].length();

    int i = 0, j = columns - 1;
    while( i < rows && j >= 0) {
        if (arr[i][j] == num) {
            return true;
        } else if (arr[i][j] > num) {
            j--;
        } else {
            i++;
        }
    }
    return false;
}
```

- C++里的字符串

```cpp
char str1[] = "hello world";
char str2[] = "hello world";
str1 == str2; // false

char *str3 = "hello world";
char *str4 = "hello world";
str3 == str4; // true
```

- [移除链表元素](https://leetcode-cn.com/problems/remove-linked-list-elements/)
  - 注意while里套的还是while
  - 为了避免麻烦，申请已经Node指向头结点

```cpp
class Solution {
public:
    ListNode* removeElements(ListNode* head, int val) {
        ListNode preHead = ListNode(0);
        preHead.next = head;
        ListNode *deleteNode = &preHead;
        while (deleteNode != NULL) {
            while (deleteNode->next && deleteNode->next->val == val) {
                deleteNode->next = deleteNode->next->next;
            }
            deleteNode = deleteNode->next;
        }
        return preHead.next;
    }
};
```

- [链表翻转打印](https://leetcode-cn.com/problems/reverse-linked-list/)
  - 如果是只打印，可以不改变链表，用栈或者递归
  - 有句话很有道理啊，递归本质上也是栈
  - 下面这个版本是翻转的，战胜51%，应该还有更好的办法

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode *pre = head, *pre2 = NULL, *next = NULL;
        while(pre) {
            next = pre->next;
            pre->next = pre2;
            pre2 = pre;
            pre = next;
        }
        return pre2;
    }
};
```
- [重构二叉树](https://leetcode-cn.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)
  - 前序和中序，或者中序和后序能构建一颗二叉树
  - 前序和后序不一定能确定

```cpp
class Solution {
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        return buildTreeIndex(preorder, 0, inorder, 0, inorder.size());
    }
private:
    TreeNode* buildTreeIndex(vector<int>& preorder, int pre_left,
                             vector<int>& inorder, int in_left, int in_length) {
        if (in_length == 0) {
            return NULL;
        } else {
            TreeNode *res = new TreeNode(preorder[pre_left]);
            int left_length = 0;
            for(;left_length < in_length; left_length++) {
                if (inorder[in_left + left_length] == preorder[pre_left]) {
                    break;
                }
            }
            res->left = buildTreeIndex(preorder, pre_left+1, inorder, in_left, left_length);
            res->right = buildTreeIndex(preorder, pre_left+1+left_length, inorder, in_left+left_length+1, in_length-left_length-1);
            return res;
        }
    }
};
```

```cpp
class Solution {
public:
    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        return buildTreeIndex(inorder, 0, postorder, 0, postorder.size());      
    }
private:
    TreeNode* buildTreeIndex(vector<int>& inorder, int in_left,
                             vector<int>& postorder, int post_left, int in_length) {
        if (in_length == 0) {
            return NULL;
        } else {         
            TreeNode *res = new TreeNode(postorder[post_left + in_length - 1]);
            int left_length = 0;
            for(;left_length < in_length; left_length++) {
                if (inorder[in_left + left_length] == postorder[post_left + in_length - 1]) {
                    break;
                }
            }
            res->left = buildTreeIndex(inorder, in_left, postorder, post_left, left_length);
            res->right = buildTreeIndex(inorder, in_left+left_length+1, postorder, post_left+left_length, in_length-left_length-1);
            return res;
        }
    }
};
```

- [用栈实现队列](https://leetcode-cn.com/problems/implement-queue-using-stacks/)
  - 顺便可以熟悉一下std stack的操作

```cpp
class MyQueue {
public:
    /** Initialize your data structure here. */
    MyQueue() {}
    
    /** Push element x to the back of queue. */
    void push(int x) {
        push_stack.push(x);
    }
    
    /** Removes the element from in front of queue and returns that element. */
    int pop() {
        int res = peek();
        pop_stack.pop();
        return res;
    }
    
    /** Get the front element. */
    int peek() {
        if (pop_stack.empty()) {
            while(!push_stack.empty()) {
                pop_stack.push(push_stack.top());
                push_stack.pop();
            }
        } 
        int res = pop_stack.top();
        return res;
    }
    
    /** Returns whether the queue is empty. */
    bool empty() {
        return push_stack.empty() && pop_stack.empty();
    }
private:
    stack<int> push_stack;
    stack<int> pop_stack;
};

/**
 * Your MyQueue object will be instantiated and called as such:
 * MyQueue* obj = new MyQueue();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->peek();
 * bool param_4 = obj->empty();
 */
```

- [用队列实现栈](https://leetcode-cn.com/problems/implement-stack-using-queues/)
  - 感觉每次判断一下q1、q2，不是很优雅

```cpp
class MyStack {
public:
    /** Initialize your data structure here. */
    MyStack() {
        
    }
    
    /** Push element x onto stack. */
    void push(int x) {
        if (q1.empty()) {
            q2.push(x);
        } else {
            q1.push(x);
        }
    }
    
    /** Removes the element on top of the stack and returns that element. */
    int pop() {
        if (q1.empty()) {
            while (q2.size() > 1) {
                q1.push(q2.front());
                q2.pop();
            }
            int res = q2.front();
            q2.pop();
            return res;
        } else {
            while (q1.size() > 1) {
                q2.push(q1.front());
                q1.pop();
            }
            int res = q1.front();
            q1.pop();
            return res;
        }
    }
    
    /** Get the top element. */
    int top() {
        if (q1.empty()) {
            while (q2.size() > 1) {
                q1.push(q2.front());
                q2.pop();
            }
            int res = q2.front();
            q1.push(q2.front());
            q2.pop();
            return res;
        } else {
            while (q1.size() > 1) {
                q2.push(q1.front());
                q1.pop();
            }
            int res = q1.front();
            q2.push(q1.front());
            q1.pop();
            return res;
        }
    }
    
    /** Returns whether the stack is empty. */
    bool empty() {
        return q1.empty() && q2.empty();
    }
private:
    queue<int> q1;
    queue<int> q2;
};

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack* obj = new MyStack();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->top();
 * bool param_4 = obj->empty();
 */
 ```

 - [旋转数组的最小值](https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/)
   - 要用二分法，注意二分的退出条件
   - 这个题目有个进阶版，就是不严格递增的情况，在mid、left、right都相等的情况下，是不能判断怎么移动的，只能退化为顺序的方法

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int ind1 = 0, ind2 = nums.size() - 1;
        int mid = ind1;
        while (nums[ind1] > nums[ind2]) {
            if (ind1 + 1 == ind2) {
                mid = ind2;
                break;
            }
            mid = (ind1 + ind2) / 2;
            if (nums[mid] < nums[ind2]) {
                ind2 = mid;
            }
            else {
                ind1 = mid;
            }
        }
        return nums[mid];
    }
};
```

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int ind1 = 0, ind2 = nums.size() - 1;
        int mid = ind1;
        while (nums[ind1] >= nums[ind2]) {
            if (ind1 + 1 >= ind2) {
                mid = ind2;
                break;
            }
            if (nums[ind1] == nums[ind2] && nums[ind1] == nums[mid]) {
                while (ind1 < ind2) {
                    ind1++;
                    if (nums[ind1] < nums[ind1 - 1]) {
                        break;
                    }
                }
                mid = ind1;
                break;
            }
            mid = (ind1 + ind2) / 2;
            if (nums[mid] <= nums[ind2]) {
                ind2 = mid;
            }
            else {
                ind1 = mid;
            }
        }
        return nums[mid];
    }
};
```

- 写一下quick sort
  - 如果社招了还让写快排，是不是在劝退了？
  - 下面这种方法是比较优雅的，还有种方法是先找左边，再找右边，然后最后交换，这种会比较直观

```cpp
void quick_sort(int *a, int l, int r) {
    if (l < r) {
        int pivot = a[l], lbk = l, rbk = r;
        while (l < r) {
            while (l < r && a[r] >= pivot) r--;
            a[l] = a[r];
            while (l < r && a[l] <= pivot) l++;
            a[r] = a[l];
        }
        a[l] = pivot;
        quick_sort(a, lbk, l - 1);
        quick_sort(a, r + 1, rbk);
    }
}
```

- [斐波那契](https://leetcode-cn.com/problems/climbing-stairs/)

```cpp
class Solution {
public:
    int climbStairs(int n) {
        if (n < 3) {
            return n;
        }
        int f1 = 1, f2 = 2;
        while (n-- > 2) {
            f2 = f1 + f2;
            f1 = f2 - f1;
        }
        return f2;
    }
};
```

- [`power(double x, int n)`]()
  - 需要注意INT_MIN的问题
  - 这里看了一个别人写的不递归的版本

```cpp
class Solution {
public:
    double myPow(double x, int n) {
        // if (n == 0) {
        //     return 1;
        // }
        // bool ispostive = n > 0;
        // n = ispostive ? n : -n;
        // double halfn = myPow(x, n >> 1);
        // double res = halfn * halfn;
        // if (n % 2 == 1) {
        //     res *= x;
        // }
        // if (!ispostive) {
        //     res = 1.0 / res;
        // }
        // return res;
        double res = 1.0;
        for (int i = n; i != 0; i /= 2) {
            if (i % 2 != 0) {
                res *= x;
            }
            x *= x;
        }
        return n < 0 ? 1 / res : res;
    }
};
```

- 位操作
  - `(n - 1) & n`，可以把最后一位1去掉
  - `(-n) & n`，可以把最后一位1保留
  
- 堆

```
priority_queue<int,vector<int>,less<int>> que; // 大顶堆
priority_queue<int,vector<int>,greater<int>> que; // 小顶堆

```

- 大顶堆是每个节点都比子节点大
- 堆排序里，升序要用大顶堆（根节点要和最后一个节点交换）
- greater和less是std实现的两个仿函数（就是使一个类的使用看上去像一个函数。其实现就是类中实现一个operator()，这个类就有了类似函数的行为，就是一个仿函数类了）

- 堆，最小的k个数，用大顶堆做
```
class Solution {
public:
    vector<int> getLeastNumbers(vector<int>& arr, int k) {
        vector<int> res(k);
        priority_queue<int,vector<int>,less<int>> que;
        for(int i = 0; i < arr.size(); i++){
            que.push(arr[i]);
            if (que.size() > k) 
                que.pop();
        }
        for(int i=k-1;i>=0;i--){
            res[i]=que.top();
            que.pop();
        }
        return res;
    }
};
```
