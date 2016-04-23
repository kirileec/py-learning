import re

def test_re():
    re1 = re.compile('\<img')

    if re1.match('< img src="www.baidu.com">asdd</img> '):
        print("Yes")

    print(re1.findall('<img src="www.baidu.com">asdd</img> '))




if __name__ == '__main__':
    test_re()