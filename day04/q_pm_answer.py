ssafy = {
    "location": ["서울", "대전", "구미", "광주"],
    "language": {
        "python": {
            "python standard library": ["os", "random", "webbrowser", 'requests'],
            "frameworks": {
                "flask": "micro",
                "django": "full-functioning"
            },
            "data_science": ["numpy", "pandas", "scipy", "sklearn"],
            "scrapying": ["requests", "bs4"],
        },
        "web" : ["HTML", "CSS"]
    },
    "classes": {
        "gm":  {
            "lecturer": "junwoo",
            "manager": "pro-gm",
            "class president": "엄윤주",
            "groups": {
                "1조": ["강대현", "권민재", "서민수", "이규진"],
                "2조": ["박재형", "서민호", "윤종원", "이지현"],
                "3조": ["김미진", "김영훈", "엄윤주", "여성우"],
                "4조": ["김교훈", "김유림", "송현우", "이현수", "진민재", "하창언"],
            }
        },
        "gj": {
            "lecturer": "change",
            "manager": "pro-gj"
        }
    }
}

#1번
# print(len(ssafy['location']))

#2번
#print('requests' in ssafy['language']['python']['python standard library'])

#3번
# print(ssafy['classes']['gm']['class president'])

#4번
# for i in ssafy['language'].keys():
#     print(i)

#5번
# for i in ssafy['classes']['gj'].values():
#     print(i)

#6번
# for k, v in ssafy['language']['python']['frameworks'].items():
#     print(f"{k}는 {v}이다.")

#7번
# import random
# a = []
# for i in ssafy['classes']['gm']['groups'].values():
#     for j in i:
#         a.append(j)
# print(random.choice(a))