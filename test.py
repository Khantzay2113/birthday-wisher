import datetime

count = 13
now = datetime.datetime.today()
if now.day == count:
    print(count)
    print('ok')
    count += 1

print(count)