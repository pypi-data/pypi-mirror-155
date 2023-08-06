def Stem2(inputW, root):
        root1 = []
        root1 = root
        root_3 = list()
        str1 = ''
        str2 = '' 
        yx = ''
        ry = ''
        for x in inputW: 
            yx += x
            for r in root:
                if yx == root['lotin']:
                    ry = root['lotin']
        str1 = inputW
        str2 = ry
        diff = str1.replace(str2, "")
        root_3.append("Input Word: "+yx+'-> Root word: '+ry+"->suffix: "+diff)
        return root_3   

def Stem(root):
    root1 = ''
    for x in root:
        root1 += root[x]

    return root1
