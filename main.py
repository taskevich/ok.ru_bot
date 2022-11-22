import OkBot


with open('accounts.txt', encoding='utf-8') as file:
    accounts = file.readlines()


account_dict = {}
for account in accounts:
    account_dict[account.split(':')[0]] = account.split(':')[1]
    

for login, password in account_dict.items():
    driver = OkBot.OkBot(login=login, password=password)
    while driver.start():
        pass
