# e.g. python prepare_data.py MultiWOZ_2.2 train
import json
import sys
import glob
import pickle
import re

input_path = sys.argv[1]
train_data_path = input_path + "/train"
dev_data_path = input_path + "/dev"
test_data_path = input_path + "/test"
data_paths = {"train": train_data_path, "dev": dev_data_path, "test": test_data_path}
data_path = data_paths[sys.argv[2]]

num_diag = 0
num_turn = 0
num_slot = 0
num_cat_slot = 0
num_noncat_slot = 0
num_cat_in_history = 0 #categorical exact matching in dialogue history
num_noncat_in_history = 0 #non-categorical exact matching in dialogue history
num_cat_in_other= 0 #categorical exact matching in training set elsewhere
num_noncat_in_other = 0 #non-categorical exact matching in training set elsewhere
num_cat_not_found = 0 #categorical not found
num_noncat_not_found = 0 #non-categorical not found
num_noncat_with_pos = 0 #non-categorical exact matching with positions
num_noncat_with_copy = 0 #non-categorical exact matching with copy from other slots
num_train = [0]*4
num_taxi = [0]*4
num_restaurant = [0]*4
num_hotel= [0]*4
num_hospital = [0]*4
num_bus = [0]*4
num_att = [0]*4
categotrical = ["restaurant-area","restaurant-bookday","restaurant-bookpeople","restaurant-pricerange",\
        "attraction-area","attraction-type","bus-day",
        "hotel-area","hotel-bookday","hotel-bookpeople","hotel-bookstay","hotel-internet","hotel-parking","hotel-pricerange","hotel-stars","hotel-type",\
        "train-bookpeople","train-day","train-departure","train-destination"] # 20 categorical slots
noncat = ["attraction-name", "restaurant-food","restaurant-name","restaurant-booktime","hotel-name", "bus-departure","bus-destination","bus-leaveat","hospital-department", \
    "train-arriveby","train-leaveat", "taxi-arriveby","taxi-departure","taxi-destination","taxi-leaveat"] # 10 noncategorical slots


'''
# collect all training utterance
train_utts = []
for f in read_files:
    with open(f,"rb") as infile:
        file_data = json.load(infile)
    for diag in file_data:
        try:
            for turn in diag["turns"]:
                train_utts.append(turn["utterance"])
        except:
            pass

with open(input_path + "/utts.train", "wb+") as outfile:
    pickle.dump(train_utts, outfile)

'''
with open(input_path + "/utts.train", "rb") as cfile:
    train_utts=pickle.load(cfile)

if "SGD" in sys.argv[1]:
    is_cat = {}
    with open(data_path + "/schema.json","rb") as sfile:
        schema = json.load(sfile)
    for ser in schema:
        for sl in ser["slots"]:
            is_cat[sl["name"]] = True if sl["is_categorical"] is True else False



read_files = glob.glob(data_path + "/dialogues*.json")

for f in read_files:
    with open(f,"rb") as infile:
        file_data = json.load(infile)
    num_diag += len(file_data)
    for diag in file_data:
        history = ""
        try: 
            for turn in diag["turns"]:
                history = history + " " + turn["utterance"]
                if turn["speaker"] == "USER":
                    num_turn += 1
                    for service in turn["frames"]:
                        num_slot += len(service["state"]["slot_values"])
                        #if service["service"] =="train": #train
                        if re.search("RideSharing", service["service"]):
                            for slot,value in service["state"]["slot_values"].items():
                                num_train[0] += 1
                                for v in value:
                                    if v in history:
                                        num_train[1] += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_train[2]+= 1
                                        break
                                    else:
                                        num_train[3] += 1
                                        break
                        #elif service["service"] == "taxi": #taxi
                        elif re.search("Flights", service["service"]):
                            for slot,value in service["state"]["slot_values"].items():
                                num_taxi[0] += 1
                                for v in value:
                                    if v in history:
                                        num_taxi[1] += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_taxi[2]+= 1
                                        break
                                    else:
                                        num_taxi[3] += 1
                                        break
                        #elif service["service"] == "restaurant": #restaurant
                        elif re.search("Restaurants", service["service"]):
                            for slot,value in service["state"]["slot_values"].items():
                                num_restaurant[0] += 1
                                for v in value:
                                    if v in history:
                                        num_restaurant[1] += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_restaurant[2]+= 1
                                        break
                                    else:
                                        num_restaurant[3] += 1
                                        break

                        #elif service["service"] == "hotel": #hotel
                        elif re.search("Hotels", service["service"]):
                            for slot,value in service["state"]["slot_values"].items():
                                num_hotel[0] += 1
                                for v in value:
                                    if v in history:
                                        num_hotel[1] += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_hotel[2]+= 1
                                        break
                                    else:
                                        num_hotel[3] += 1
                                        break
                        elif service["service"] == "hospital":
                            for slot,value in service["state"]["slot_values"].items():
                                num_hospital[0] += 1
                                for v in value:
                                    if v in history:
                                        num_hospital[1] += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_hospital[2]+= 1
                                        break
                                    else:
                                        num_hospital[3] += 1
                                        break
                        elif service["service"] == "bus":
                            for slot,value in service["state"]["slot_values"].items():
                                num_bus[0] += 1
                                for v in value:
                                    if v in history:
                                        num_bus[1] += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_bus[2]+= 1
                                        break
                                    else:
                                        num_bus[3] += 1
                                        break
                        #elif service["service"] == "attraction": #attraction
                        elif re.search("Movies", service["service"]):
                            for slot,value in service["state"]["slot_values"].items():
                                num_att[0] += 1
                                for v in value:
                                    if v in history:
                                        num_att[1] += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_att[2]+= 1
                                        break
                                    else:
                                        num_att[3] += 1
                                        break

                        for slot,value in service["state"]["slot_values"].items():
                            #if non-categorical
                            if is_cat[slot] is False:
                            #if slot in noncat:
                                num_noncat_slot += 1
                                for annot in service["slots"]:
                                    if slot == annot["slot"] and "exclusive_end" in annot.keys():
                                        num_noncat_with_pos += 1 
                                    else: 
                                    #elif slot == annot["slot"] and "copy_from" in annot.keys():
                                        num_noncat_with_copy += 1 
                                for v in value:
                                    if v in history:
                                        num_noncat_in_history += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_noncat_in_other += 1
                                        break
                                    else:
                                        num_noncat_not_found += 1
                                        break
                            #if categorical
                            else:
                                num_cat_slot += 1
                                for v in value:
                                    if v in history:
                                        num_cat_in_history += 1
                                        break
                                    elif any(v in utt for utt in train_utts):
                                        num_cat_in_other += 1
                                        break
                                    else:
                                        num_cat_not_found += 1
                                        break
            #print(diag)
            #print(history)
            #print(num_cat_in_history)
            #print(num_cat_in_other)
            #print(num_noncat_in_history)
            #print(num_noncat_in_other)
            #raise Exception("Single dialogue")
        except:
            num_diag -= 1
            print(diag)
            raise Exception("no turns in above dialogue.")

print("Total dialogues: {}.".format(num_diag))
print("Total turns: {}.".format(num_turn))
print("Total slots: {}.".format(num_slot))
print("Total slots in history/slots: {}/{}, {}.".format(num_cat_in_history + num_noncat_in_history,num_cat_slot + num_noncat_slot, (num_cat_in_history + num_noncat_in_history)/(num_cat_slot + num_noncat_slot)))
print("Total slots somewhere else/slots: {}/{}, {}.".format(num_cat_in_other + num_noncat_in_other,num_cat_slot + num_noncat_slot, (num_cat_in_other + num_noncat_in_other)/(num_cat_slot + num_noncat_slot)))
print("Total slots not found/slots: {}/{}, {}.".format(num_cat_not_found + num_noncat_not_found,num_cat_slot + num_noncat_slot, (num_cat_not_found + num_noncat_not_found)/(num_cat_slot + num_noncat_slot)))
print("-"*8)
print("categorical v.s. non-categorical:")
print("categorical_in_history/categorical: {}/{}, {}.".format(num_cat_in_history,num_cat_slot, num_cat_in_history/num_cat_slot))
print("categorical_somewhere_else/categorical: {}/{}, {}.".format(num_cat_in_other,num_cat_slot, num_cat_in_other/num_cat_slot))
print("categorical_not_found/categorical: {}/{}, {}.".format(num_cat_not_found,num_cat_slot, num_cat_not_found/num_cat_slot))
print("noncategorical_in_history/noncategorical: {}/{}, {}.".format(num_noncat_in_history,num_noncat_slot, num_noncat_in_history/num_noncat_slot))
print("noncategorical_somewhere_else/noncategorical: {}/{}, {}.".format(num_noncat_in_other,num_noncat_slot, num_noncat_in_other/num_noncat_slot))
print("noncategorical_not_found/noncategorical: {}/{}, {}.".format(num_noncat_not_found,num_noncat_slot, num_noncat_not_found/num_noncat_slot))
print("noncategorical_with_pos_annotation/noncategorical: {}/{}, {}.".format(num_noncat_with_pos,num_noncat_slot, num_noncat_with_pos/num_noncat_slot))
print("noncategorical_with_copy_annotation/noncategorical: {}/{}, {}.".format(num_noncat_with_copy,num_noncat_slot, num_noncat_with_copy/num_noncat_slot))
print("-"*8)
print("in_hitory, somewhere_else, not_found:")
print("Train: {},{},{}".format(num_train[1]/num_train[0], num_train[2]/num_train[0], num_train[3]/num_train[0]))
print("Taxi: {},{},{}".format(num_taxi[1]/num_taxi[0], num_taxi[2]/num_taxi[0], num_taxi[3]/num_taxi[0]))
print("Restaurant: {},{},{}".format(num_restaurant[1]/num_restaurant[0], num_restaurant[2]/num_restaurant[0], num_restaurant[3]/num_restaurant[0]))
print("Hotel: {},{},{}".format(num_hotel[1]/num_hotel[0], num_hotel[2]/num_hotel[0], num_hotel[3]/num_hotel[0]))
#print("Hospital: {},{},{}".format(num_hospital[1]/num_hospital[0], num_hospital[2]/num_hospital[0], num_hospital[3]/num_hospital[0]))
#print("Bus: {},{},{}".format(num_bus[1]/num_bus[0], num_bus[2]/num_bus[0], num_bus[3]/num_bus[0]))
print("Attraction: {},{},{}".format(num_att[1]/num_att[0], num_att[2]/num_att[0], num_att[3]/num_att[0]))
