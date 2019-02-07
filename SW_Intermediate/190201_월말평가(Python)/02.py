# 파일명 변경 금지
# 아래에 클래스를 Point와 Rectangle을 선언하세요.
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:

    def __init__(self, p1, p2):
        self.p1 = (p1.x, p1.y)
        self.p2 = (p2.x, p2.y)

    def get_area(self):
        return (self.p2[0]-self.p1[0]) * (self.p1[1]-self.p2[1])

    def get_perimeter(self):
        return (self.p2[0]-self.p1[0]+self.p1[1]-self.p2[1])*2

    def is_square(self):
        if (self.p2[0]-self.p1[0]) == (self.p1[1]-self.p2[1]):
            return True
        else:
            return False


# 아래의 코드는 수정하지마세요. 
if __name__ == '__main__':
    p1 = Point(1, 3)
    p2 = Point(3, 1)
    r1 = Rectangle(p1, p2)
    print(r1.get_area())
    print(r1.get_perimeter())
    print(r1.is_square())
    p3 = Point(2, 5)
    p4 = Point(8, 3)
    r2 = Rectangle(p3, p4)
    print(r2.get_area())
    print(r2.get_perimeter())
    print(r2.is_square())