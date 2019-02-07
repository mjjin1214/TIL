# 파일명 변경 금지
def cipher(word, n):
    # 아래에 코드를 작성하시오.
    # word는 모두 소문자로만 구성되어 있습니다.
    # n은 양의 정수입니다.
    # 암호화된 문자열을 반환합니다.
    s = ''
    for i in word:
        d = ord(i)+(n % 26)
        if d > 122:
            d -= 26
        s += chr(d)

    return s

    # result += chr((ord(word) - 97 + n) % 26 + 97)


# 아래의 코드는 수정하지마세요. 
if __name__ == '__main__':
    print(cipher('apple', 1))
    print(cipher('apple', 53))
    print(cipher('zoo', 2))