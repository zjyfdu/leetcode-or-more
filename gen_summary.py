import os

print("# Summary\n")

lines = []
for root, dirs, files in os.walk("."):
    # print(root, dirs, files)
    if root == '.':
        for f in files:
            if f.endswith('.md'):
                print("* [{0}]({1})".format(f[:-3], f))
    elif any([x.endswith('.md') for x in files]):
        print("* [{}]()".format(root[2:]))
        for f in files:
            if f.endswith('.md'):
                print("\t* [{0}]({1})".format(f[:-3], f))