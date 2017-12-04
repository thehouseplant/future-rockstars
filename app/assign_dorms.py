import json
import math
import random

db = open('./data/members.json', 'r')

db_manage_total = json.loads(db.read())
db.close()

# initialize the semester
semester_value = 1

if semester_value == 1:
    dorm_db = open('./data/dorms.json', 'w')
    db_exist = []
else:
    dorm_db = open('./data/dorms.json', 'r')
    db_exist = json.loads(dorm_db.read())
    dorm_db.close()
    dorm_db = open('./data/dorms.json','w')
    db_exist = db_exist[0:(6*(semester_value-1))]

if semester_value == 1:
    temp_semester = 'first'
elif semester_value == 2:
    temp_semester = 'second'
else:
    temp_semester = 'third'

db_manage = []
for data in db_manage_total:
    if data['cohort'] == temp_semester:
        db_manage.append(data)
print(len(db_manage))


boy_oldCampers,boy_middleCampers,boy_youngCampers = [],[],[]
girl_oldCampers,girl_middleCampers,girl_youngCampers = [],[],[]
boy_dorm,girl_dorm,total_dorm = [],[],[]

# separate the members into different age


def age_judge(age_range, target):
    min_age = age_range[0]
    max_age = age_range[1]
    temp_judge = int(target.get('age'))
    temp_member = str(target.get('memberId')) +' || '+ str(target.get('age')) + \
        ' || ' + target.get('firstName') + ' ' + target.get('lastName')
    if temp_judge >= min_age and temp_judge <= max_age:
        return temp_member
    else:
        return 0

# assign dorms with age and gender


def gender_separate(gender_list):
    member_loop = math.ceil(len(gender_list[0]) / 3) + math.ceil(len(gender_list[2]) / 3)
    member_list = [[], [], []]
    if member_loop < 8:
        extra_loop = 0
    else:
        extra_loop = member_loop - 8
        member_loop = 8
    for loop in range(member_loop):
        i = divmod(loop, 2)[1]
        if i == 0:
            i = 0
            if len(gender_list[0]) == 0 :
                i = 2
        elif i == 1:
            i = 2
            if len(gender_list[2]) == 0:
                i = 0
        for j in range(3):
            if len(gender_list[i]) != 0:
                member_list[j].append(gender_list[i][0])
                del gender_list[i][0]
            elif len(gender_list[1]) != 0:
                member_list[j].append(gender_list[1][0])
                del gender_list[1][0]
    for loop in range(extra_loop):
        extra_list = []
        for i in range(3):
            if len(gender_list[i]) != 0:
                extra_list.append(gender_list[i])
        j = 0
        while j < 3:
            if len(member_list[j]) < 8:
                member_list[j].append(extra_list[0])
                del extra_list[0]
            j += 1
    member_small = math.ceil(len(gender_list[1]) / 3)
    for loop in range(member_small):
        for j in range(3):
            if len(gender_list[1]) == 0:
                break
            elif len(member_list[j]) < 8:
                member_list[j].append(gender_list[1][0])
                del gender_list[1][0]
    return member_list

# random each gender separate result


def random_result(gender_list):
    for i in range(len(gender_list)):
        random.shuffle(gender_list[i])
    return gender_list


boy_list = [boy_youngCampers, boy_middleCampers, boy_oldCampers]
girl_list = [girl_youngCampers, girl_middleCampers, girl_oldCampers]
# separate members into different gender
age_case = [[13, 14], [15, 16], [17, 18]]
for i in range(len(db_manage)):
    if db_manage[i].get('gender') == 'male':
        for j in range(len(age_case)):
            temp = age_judge(age_case[j], db_manage[i])
            if temp != 0:
                boy_list[j].append(temp)
    if db_manage[i].get('gender') == 'female':
        for j in range(len(age_case)):
            temp = age_judge(age_case[j], db_manage[i])
            if temp != 0:
                girl_list[j].append(temp)

boy_list = random_result(boy_list)
girl_list = random_result(girl_list)


# separate boys into their own dorm_member
boy_member_list = gender_separate(boy_list)

# separate girls into their own dorm_member
girl_member_list = gender_separate(girl_list)


# import each member into their dorm
for i in range(3):
    dorm_name = "boy-dorm" + " " + str(i+3*(semester_value-1))
    boy_dorm.append({'name': dorm_name, 'type': 'dorm',
                     'gender': 'male', 'members': boy_member_list[i]})
for i in range(3):
    dorm_name = "girl-dorm" + " " + str(i+3*(semester_value-1))
    girl_dorm.append({'name': dorm_name, 'type': 'dorm',
                      'gender': 'female', 'members': girl_member_list[i]})

total_dorm = boy_dorm + girl_dorm
total_dorm = json.dumps(db_exist + total_dorm)
dorm_db.write(total_dorm)
dorm_db.close()

