from datetime import datetime

date1 = datetime.now()
date2 = datetime(day=1, month=9, year=2022)

timedelta = (date1 - date2)// 7
print(timedelta.days )

if (timedelta.days % 2) != 0:
    print( "Числитель")
else:
    print("Знаменатель")
