import json
import random
import math

def member_test(file):
    db = open('./data/members_test.json','r')
    db_manage_totals = json.loads(db.read())
    db_manage_totals = db_manage_totals['members']
    db.close()
    return db_manage_totals

db = open('./data/members.json', 'r')
db_manage_total = json.loads(db.read())
db.close()

#for test
#db_manage_total = member_test('./data/members_test.json')

# initialize the semester
semester_value = 1

if semester_value == 1:
    band_db = open('./data/bands.json','w')
    band_exist = []
    band_number = 0
    print(len(db_manage_total))
    for memberss in range(len(db_manage_total)):
        db_manage_total[memberss]['status'] = 'Submitted'
        
else:
    band_exist = []
    band_db = open('./data/bands.json','r')
    band_exists = json.loads(band_db.read())
    for i in range(len(band_exists)):
        semester = band_exists[i].get('cohort')
        if semester == 'first':
            semester = 1
        elif semester == 'second':
            semester = 2
        elif semester =='third':
            semester = 3 
        if semester < semester_value:
            band_exist.append(band_exists[i])
    band_db.close()
    band_db = open('./data/bands.json','w')
    band_number = len(band_exist)

# initialize the data
band_list,singer_list,guitar_list,drummer_list = [],[],[],[]
bassist_list,keyboardist_list,instrument_list = [],[],[]

# grade the gender, male=0, female=1


def male_female_grade(type_list):
    total = []
    for i in range(len(type_list)):
        if type_list[i]['gender'] == 'male':
            total.append(0)
        elif type_list[i]['gender'] == 'female':
            total.append(1)
    return total

# judge whether the female or male is free to choose. free=2, If not free,male=0,female=1. If no data = -1


def male_female_judge(type_list):
    j = 0
    for i in type_list:
        j = j + i
    if len(type_list) == 0:
        judge_result = -1
    elif j == len(type_list):
        judge_result = 1
    elif j == 0:
        judge_result = 0
    elif j < len(type_list):
        judge_result = 2
    return judge_result

# create the list to judge whether the talent rank is free to choose in each gender


def type_ruler(member, gender):
    if gender == 'male':
        g = 0
    else:
        g = 1
    ruler = [[0, 0, 0, 0, g], [0, 0, 0, 0, g], [0, 0, 0, 0, g],
             [0, 0, 0, 0, g], [0, 0, 0, 0, g], [0, 0, 0, 0, g]]
    for i in range(len(member)):
        for j in range(len(member[i])):
            if member[i][j].get('gender') == gender:
                templ = member[i][j].get('trank')
                ruler[i][templ - 1] = templ
    return ruler

# gender choose & remove


def member_result(type_member, gender, rank):
    for i in range(len(type_member)):
        if type_member[i].get('gender') == gender and type_member[i].get('trank') == rank:
            temp_memberls = type_member[i].get('member_info')
            IDs = type_member[i].get('member_info').split('||')[0]
            for j in range(len(db_manage_total)):
                if int(db_manage_total[j]['memberId']) == int(IDs):
                    db_manage_total[j]['status'] ='Accepted'
                    break
            del type_member[i]
            break
    return temp_memberls

# Average


def average(list):
    sum = 0
    length = 0
    for i in list:
        if i == 'null':
            pass
        elif i != 0:
            sum = sum + i
            length += 1
    if length != 0:
        return sum / length
    else:
        return 0

# input band by their talent rank


def band_rank(ruler_boy, ruler_girl, result):
    talent_list = []
    talent_grade = 0
    k = 0
    for i in range(6):
        talent_list.append(0)
        if result[i] == 0:
            for j in range(4):
                if i == 0 and ruler_boy[i][j] != 0:
                    talent_list[i] = ruler_boy[i][j]
                    break
                if ruler_boy[i][j] != 0:
                    talent_list[i] = ruler_boy[i][j]
                    ave_add = average(talent_list)
                    var_add = variance(talent_list, ave_add)
                    var_balance = abs(var_add - 1.25)
                    if var_balance < 0.2:
                        if len(talent_list) > 3:
                            if ave_add >2.7:
                                talent_list[-1] = 0
                            else:
                                break
                        else:
                            break
                    else:
                        talent_list[-1] = 0
        if result[i] == 1:
            for j in range(4):
                if i == 'null':
                    talent_list[i] = 'null'
                    break
                elif k == 0 and ruler_girl[i][j] != 0:
                    talent_list[i] = ruler_girl[i][j]
                    k=1
                    break
                if ruler_girl[i][j] != 0:
                    talent_list[i] = ruler_girl[i][j]
                    ave_add = average(talent_list)
                    var_add = variance(talent_list, ave_add)
                    var_balance = abs(var_add - 1.25)
                    if var_balance < 0.35:
                        if len(talent_list) > 3:
                            if ave_add >2.7:
                                talent_list[-1] = 0
                            else:
                                break
                        else:
                            break
                    else:
                        talent_list[-1] = 0
        if result[i] == 'null':
            talent_list[i] = 'null'
        if talent_list[i] == 0:
            talent_grade+=1
    talent_list.append(talent_grade)
    return talent_list

# variance


def variance(list, average):
    sum = 0
    length = 0
    for i in list:
        if i == 'null':
            pass
        elif i != 0:
            sum = sum + (i - average)**2
            length += 1
    if length != 0:
        return sum / length
    else:
        return 0

# input the gender result


def result_list(best_number, judge_list):
    result = []
    for j in range(len(judge_list) - 1):
        if judge_list[j] == 2:
            if best_number < 1:
                result.append(0)
            else:
                result.append(1)
                best_number -= 1
        if judge_list[j] == 0:
            result.append(0)
        if judge_list[j] == 1:
            result.append(1)
        if judge_list[j] == -1:
            result.append('null')
    result.append(judge_list[-1])
    return result

#Choose the semester
def semester(sem):
    db_manage = []
    db_old = []
    sem_temp = 0 
    temp_request = []
    for i in range(len(db_manage_total)):
        semester = db_manage_total[i].get('cohort')
        if semester == 'first':
            semester = 1
        elif semester == 'second':
            semester = 2
        elif semester =='third':
            semester = 3 
        if semester == sem:
            if db_manage_total[i].get('requestedMember') == '':
                db_manage.append(db_manage_total[i])
            else:
                temp_request.append(db_manage_total[i])
        elif semester < sem and db_manage_total[i].get('status') == 'Waitlisted':
            db_old.append(db_manage_total[i])
    random.shuffle(db_manage)
    if db_old != []:
        db_manage = db_old + db_manage
    print(len(db_manage))
    request_num = len(temp_request)

    for i in range(request_num):
        first_member = temp_request[i]
        for j in temp_request:
            if j['memberId'] == temp_request[i]['requestedMember']:
                second_member = j
        if int(first_member['memberId']) > int(second_member['memberId']):
            pass
        else:
            extra_request.append({'talent':[first_member['talent'],second_member['talent']],'info':[first_member,second_member]})
    print(len(db_old))
    return db_manage

#Get specific information from db_manage(all member info)
def getmember(data):
    all_members = [[],[],[],[],[],[]]
    for i in range(len(data)):
        id_name = db_manage[i].get('memberId') + " || " + \
        db_manage[i].get('gender')
        temp = {'gender': db_manage[i].get('gender'), 'trank': db_manage[i].get('trank'), 'member_info': id_name + " || " +
                db_manage[i].get('firstName') + " " + db_manage[i].get('lastName') + " || " + str(db_manage[i].get('trank'))}
        if db_manage[i].get('talent') == 'Singer':
            all_members[0].append(temp)
        elif db_manage[i].get('talent') == 'Guitarist':
            all_members[1].append(temp)
        elif db_manage[i].get('talent') == 'Drummer':
            all_members[2].append(temp)
        elif db_manage[i].get('talent') == 'Bassist':
            all_members[3].append(temp)
        elif db_manage[i].get('talent') == 'Keyboardist':
            all_members[4].append(temp)
        elif db_manage[i].get('talent') == 'Instrumentalist':
            all_members[5].append(temp)
    return all_members

#Use for the process to deal with the people who are not match
def talent_extra(tr,gender_ruler,nm,type,gender_list):
    var_first = 0
    for s_add in range(4):
        if gender_ruler[nm][s_add] != 0:
            if var_first == 0:
                tr[nm] = gender_ruler[nm][s_add]
                ave = average(tr)
                var_small = abs(variance(tr,ave) - 1.25)
                var_first+=1
            else:
                if gender_ruler[nm][s_add] == 0:
                    pass
                else:
                    tr[nm] = gender_ruler[nm][s_add]
                    ave = average(tr)
                    var = abs(variance(tr,ave)-1.25)
                    if var < var_small:
                        var_small = var
        elif s_add == 3 and var_first == 0:
            if type == 'boy':
                gender_list[nm] = 1
                return talent_extra(tr,ruler_girl,nm,'girl',gender_list)
            elif type == 'girl':
                gender_list[nm] = 0
                return talent_extra(tr,ruler_boy,nm,'boy',gender_list)
    return tr

extra_request = []

# input data into each dataset type. Change this will change the input to achieve that each semester get the different result
db_manage = semester(semester_value)

# The max number of bands
band_amount = math.ceil(len(db_manage) / 6)

all_member = getmember(db_manage)
for ff in range(6):
    print(len(all_member[ff]))
band_gradelist = []

key = ['Singer', 'Guitarist', 'Drummer',
       'Bassist', 'Keyboardist', 'Instrumentalist']


# generate the result
for i in range(band_amount):
    band_numberstr = str(band_number)
    balance_number = 6
    band_name = "band " + band_numberstr
    band_number+=1
    if semester_value == 1:
        semester_value = 'first'
    elif semester_value == 2:
        semester_value = 'second'
    elif semester_value == 3:
        semester_value = 'third'
    band_list.append({"name": band_name, "type": "band","cohort":semester_value})
    final_result = []

    # find the balance_number(current people can choose) and best_number(the best number of girl to choose)
    # then input the judge list
    judge_list_f = []
    for n in all_member:
        temp_list = male_female_grade(n)
        temp_number = male_female_judge(temp_list)
        if temp_number == -1:
            balance_number -= 1
        if temp_number == 1:
            balance_number -= 2
        judge_list_f.append(temp_number)
    if balance_number < 1:
        balance_number = 0
    best_number = int(balance_number / 2)

    # input the number of how many times that judge_list can change(each 2 get 1)
    change_grade = 0
    for grade_judge in judge_list_f:
        if grade_judge == 2:
            change_grade += 1
    judge_list_f.append(change_grade)

    # first run
    ruler_boy = type_ruler(all_member, 'male')
    ruler_girl = type_ruler(all_member, 'female')
    result = result_list(best_number, judge_list_f)
    talent_list = band_rank(ruler_boy, ruler_girl, result)

    # if the first talent result doesn't reasonable, then do a loop to find the best reasonable talent list
    # talent_list[-1] means: the amount of 0, which people's talent rank doesn't match the whole list
    # result[-1] means: the amount of 2, which the number of gender can change
    if talent_list[-1] == 0:
        final_result = result + talent_list
    elif result[-1] == 0:
        final_result = result + talent_list
    else:
        nofree = []
        char_val = 0
        for char in judge_list_f[:-1]:
            if char != 2:
                nofree.append(char_val)
            char_val += 1
        free_num = int(result[-1] / 2)
        talent_min = talent_list
        result_min = result
        small = talent_list[-1]

        # start the loop for each judge_list
        for num in range(2**free_num):
            change_list = bin(num)[2:]
            if len(change_list) < free_num:
                change_list = '0'*(free_num-len(change_list)) + change_list
            change_list = change_list + '0' * int((6 - len(nofree))/2)
            if len(nofree)/2-int(len(nofree)/2) !=0:
                for kl in range(6):
                    if kl in nofree:
                        pass
                    else:
                        nofree.append(kl)
                        break
            result_R = []
            best_number_temp = best_number
            state = 0
            # by using the change list to change the gender judge list, if value ==0, don't change. If value ==1,change
            for small_extra in range(6):
                if small_extra in nofree:
                    if judge_list_f[small_extra] == 0:
                        result_R.append(0)
                    elif judge_list_f[small_extra] == 1:
                        result_R.append(1)
                    elif judge_list_f[small_extra] == -1:
                        result_R.append('null')
                    elif judge_list_f[small_extra] == 2:
                        result_R.append(1)                        
                else:
                    if change_list[state] == '0':
                        state += 1
                        if best_number_temp < 1:
                            result_R.append(0)
                        else:
                            result_R.append(1)
                            best_number_temp -= 1
                    elif change_list[state] == '1':
                        state += 1
                        if best_number_temp < 1:
                            result_R.append(1)
                            best_number_temp -= 1
                        else:
                            result_R.append(0)
            talent_list_R = band_rank(ruler_boy, ruler_girl, result_R)
            if small > talent_list_R[-1]:
                talent_min = talent_list_R
                small = talent_list_R[-1]
                result_min = result_R
                if small == 0:
                    result_min.append(0)
                    break
        if len(result_min) == 6:
            result_min.append(0)
        final_result = result_min + talent_min
    
    #generate people who didn't match after normal algorithm 
    band_gradelist.append(final_result)

    # write the whole result into band_list, which will write into the json file after all done
    for ti in range(6):
        if final_result[ti] == 0:
            if final_result[ti + 7] == 0:
                band_list[i][key[ti]] = 'matching'
            else:
                band_list[i][key[ti]] = member_result(
                    all_member[ti], 'male', final_result[ti + 7])
        elif final_result[ti] == 1:
            if final_result[ti + 7] == 0:
                band_list[i][key[ti]] = 'matching'
            else:
                band_list[i][key[ti]] = member_result(
                    all_member[ti], 'female', final_result[ti + 7])
        else:
            band_list[i][key[ti]] = 'null, already assign all people'

print(band_gradelist)
#process the people who didn't match after normal algorithm
ruler_boy = type_ruler(all_member, 'male')
ruler_girl = type_ruler(all_member, 'female')
band_nomatchlist = []
band_nomatch_name = []
print(extra_request)

re_key= {'Singer':0, 'Guitarist':1, 'Drummer':2,
       'Bassist':3, 'Keyboardist':4, 'Instrumentalist':5}
band_num = 0
for i in band_list:
    sum = 0
    for j in key:
        if i[j] == 'matching':
            sum +=1
            if i['name'] in band_nomatch_name:
                pass
            else:
                band_nomatch_name.append(i['name'])
            for ms in range(len(extra_request)):
                if extra_request[ms] != []:
                
                    m = extra_request[ms]
                    for t in range(2):
                        if m['talent'][t] == j:
                            if i[m['talent'][1-t]] == 'matching':
                                sum-=2
                                i[j] = m['info'][t]['memberId'] + ' || ' +m['info'][t]['firstName'] + m['info'][t]['lastName'] + ' || ' + str(m['info'][t]['trank'])
                                i[m['talent'][1-t]] =  m['info'][1-t]['memberId'] + ' || ' +m['info'][1-t]['firstName'] + m['info'][1-t]['lastName'] + ' || ' + str(m['info'][1-t]['trank'])
                                print(band_gradelist[band_num])
                                band_gradelist[band_num][-1]-=2
                                if m['info'][t]['gender'] == 'male':
                                    band_gradelist[band_num][re_key[j]] = 0
                                    band_gradelist[band_num][re_key[m['talent'][1-t]]] = 0
                                else:
                                    band_gradelist[band_num][re_key[j]] = 1
                                    band_gradelist[band_num][re_key[m['talent'][1-t]]] = 1
                                band_gradelist[band_num][re_key[j]+7] = m['info'][t]['trank']
                                band_gradelist[band_num][re_key[m['talent'][1-t]]+7] = m['info'][t]['trank']
                                print(band_gradelist[band_num])
                                extra_request[ms] = []
                                break
    print(band_num)
    if sum == 0:
        del band_nomatch_name[-1]
        del band_gradelist[band_num] 
    band_num +=1                   

for i in band_gradelist:
    if i[-1]==0:
        pass
    else:
        band_nomatchlist.append(i)

print(band_nomatchlist)

#After first run, deal with the people who are not match the algorism
for i in range(len(band_nomatchlist)):
    print(i)
    if i == 7:
        print(all_member)
    gender_result = band_nomatchlist[i][0:6]
    talent_result = band_nomatchlist[i][7:13]
    for num in range(6):
        person_chan =[0,0]
        if talent_result[num] == 0:
            if gender_result[num] == 0:
                talent_result = talent_extra(talent_result,ruler_boy,num,'boy',gender_result)
            elif gender_result[num] == 1:
                talent_result = talent_extra(talent_result,ruler_girl,num,'girl',gender_result)
            person_chan[0] = gender_result[num]
            person_chan[1] = talent_result[num]
            for name in band_list:
                if name['name'] == band_nomatch_name[i]:
                    for keys in range(len(key)):
                        if name[key[keys]] == 'matching':
                            if person_chan[0] == 0:
                                gender = 'male'
                            else:
                                gender = 'female'
                            name[key[keys]] = member_result(all_member[keys], gender, person_chan[1])
                            ruler_boy = type_ruler(all_member, 'male')
                            ruler_girl = type_ruler(all_member, 'female')
                            break

# result input
band_list = band_exist + band_list
band_list = json.dumps(band_list)
band_db.write(band_list)
band_db.close()
db = open('./data/members.json', 'w')
db_manage_total = json.dumps(db_manage_total)
db.write(db_manage_total)
db.close()

