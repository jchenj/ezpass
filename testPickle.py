import passman
import pickle


#! TODO: how to add multiple class instances to file?

fname = 'testfile.csv'
ac1 = 'myAccount1'
p1 = "pass1"

account1 = passman.Account(fname, ac1, p1)

ac2 = 'myAccount2'
p2 = 'mypass2'

account2 = passman.Account(fname, ac2, p2)
aclist = [account1, account2]

with open(fname, 'wb') as file:
    pickle.dump(aclist, file)


with open(fname, 'rb') as file:
    unserial = pickle.load(file)

print(unserial[0].__dict__)
# print(type(account1) == type(unserial))
# print(type())
# print(unserial.__dict__)
# print(account1.__dict__ == unserial.__dict__)



#


# for account in aclist:
#     pickle.dump(account, file)