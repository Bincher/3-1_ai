"""
1주차 - 실습 : 튜플 패킹
"""

def Sum(*nums):
    num_pos = 0
    num_neg = 0
    for i in nums:
        if i > 0 :
            num_pos += i
        else:
            num_neg += i

    return (num_pos, num_neg)

print(Sum(1, -2, 3.6, 5, -8.2, 4))
print(Sum(4, 2.5, -2, 4))
