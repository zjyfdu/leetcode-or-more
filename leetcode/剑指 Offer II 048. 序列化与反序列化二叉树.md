
二叉树的序列化和反序列化

用层序遍历是可以做的

但是cpp的string没有split，实现起来比较麻烦

```
string::size_type left = data.find_first_not_of(" ", 0);
string::size_type right = data.find_first_of(" ", left);
cout << (string::npos != left) << " " << (string::npos != right) << endl;
while (string::npos != left || string::npos != right) {
    string tmp = data.substr(left, right-left);
    if (tmp == "N") {
        vec.push_back(NULL);
    } else {
        vec.push_back(new TreeNode(stoi(tmp)));
    }
    left = data.find_first_not_of(" ", right);
    right = data.find_first_of(" ", left);
}
```


```
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Codec {

public:

    // Encodes a tree to a single string.
    string serialize(TreeNode* root) {
        string res;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            TreeNode* t = q.front();
            q.pop();
            if (t == nullptr) {
                res += " N";
            } else {
                res += " " + to_string(t->val);
                q.push(t->left);
                q.push(t->right);
            }
        }
        return res;
    }

    // Decodes your encoded data to tree.
    TreeNode* deserialize(string data) {
        vector<TreeNode*> vec;
        string::size_type lastPos = data.find_first_not_of(" ", 0);
        string::size_type pos = data.find_first_of(" ", lastPos);
        while (string::npos != pos || string::npos != lastPos) {
            string val = data.substr(lastPos, pos - lastPos);
            if (val == "N") {
                vec.push_back(NULL);
            } else {
                vec.push_back(new TreeNode(stoi(val)));
            }
            lastPos = data.find_first_not_of(" ", pos);
            pos = data.find_first_of(" ", lastPos);
        }
        int i = 0, j = 1;
        for (; j < vec.size(); ++i) {             
            if (vec[i] == NULL) continue;
            if (j < vec.size()) vec[i]->left = vec[j++];
            if (j < vec.size()) vec[i]->right = vec[j++];
        }
        return vec[0];
    }
};

// Your Codec object will be instantiated and called as such:
// Codec ser, deser;
// TreeNode* ans = deser.deserialize(ser.serialize(root));
```