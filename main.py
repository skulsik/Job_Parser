from Lib.GetVacancy import HH, SuperJob
from Lib.Errors import Error
import json # Убрать

# HH.ru

HH_ru = HH('python junior')
hh_requests_list = HH_ru.get_request()

j = 0
for i in hh_requests_list:
    j += 1
    print(i['name'])
print(j)

# SuperJob

SJ = SuperJob('программист')
sj_requests_list = SJ.get_request()

j = 0
for i in sj_requests_list:
    j += 1
    print(i['profession'])
print(j)

#print(json.dumps(sj_requests_list, indent=2, ensure_ascii=False))
