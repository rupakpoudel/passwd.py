import shelve
import hashlib,sys
from getpass import getpass

class PasswordManager:

    database=shelve.open("database")

    def __init__(self):
        while True:
            try:
                with open("masterpass.txt",'r') as obj:
                    obj.read()
            except FileNotFoundError:
                self.set_master_pass()
            if self.validate_user():break
            else:
                trying=input("Password incorrect want try again: Y/N ?\n")
                if trying.lower()=='y':continue
                else:sys.exit()
        if self.ask_input().upper()=="GET":
            self.ask_user_input("get")
        else:
            self.ask_user_input("put")

    def set_master_pass(self):
        password=getpass("Enter your new password")
        password_again=getpass("Verify your passoword")
        if password==password_again:
            hashpass=hashlib.sha256(password.encode())
            hashpass=hashpass.hexdigest()
            with open("masterpass.txt","w") as f_obj:
                f_obj.write(hashpass)

    def ask_user_input(self,type):
        platform=input("Enter platform ?")
        username=input("Enter user name ?")
        if type=="put":
            password=input("Enter password you want to store ")
            self.add_pass(platform,username,password)
        else:
            self.show_password(platform,username)

    def ask_input(self):
        return input("Do you want to get or put data ? (GET/PUT)\n")

    def validate_user(self):
        passwd=getpass("Input master password:-")
        hash=hashlib.sha256(passwd.encode())
        hash=hash.hexdigest()

        masthash=open('masterpass.txt','r').read()
        if hash==masthash.split('\n')[0]:
            return True
        else:
            return False


    def add_pass(self,platform,user,passwd):
        self.database.update({platform:{user:passwd}})

    def show_password(self,app,user):
        try:
            password=self.database[app][user]
        except KeyError:
            self.error_code(f"Username {user} not found for appliction {app}")
            if input("Do you want to ad user ? Y/N").lower()=='y':
                self.ask_user_input('put')
        else:
            self.show_output(f"Your password for username {user} is "+password)

    def show_output(self,output):
        print(output)

    def error_code(self,message):
        print(message)

if __name__ == '__main__':
    PasswordManager()