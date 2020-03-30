import socket

class HangmanClient:
     def __init__(self, IP, port):
        """The code for hangman client."""
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect((IP,port))
            print("Enter your name")
            details = input()
            self.s.send(("Start " + details).encode())
            m = self.s.recv(1024).decode()
            #print("check1:")
            print(m)
            while (("You are a new user") in m):
                a = input()
                if (a != 'yes'):
                    print("Sorry, You cannot play the game with out registration.")
                    continue
                else:
                    self.s.send(a.encode())
                    break
            if (('Please guess a letter:') in m):
                    #print("abc")
                    self.s.send(input().encode())

            while 1:
                message = self.s.recv(1024).decode()
                #print("check2")
                print(message)
                if (('Congratulations, you won!') in message or ('Sorry you ran out of guesses') in message):
                    print('If you want to see the leader board type Y')
                    self.s.send(input().encode())
                    data = self.s.recv(1024).decode()
                    print(data)
                    break
                elif (('Please guess a letter:') in message):
                    #print("abc")
                    self.s.send(input().encode())
            self.s.close()                 
def main():
    HangmanClient('', 2525)
if __name__ == "__main__":
    main()              
