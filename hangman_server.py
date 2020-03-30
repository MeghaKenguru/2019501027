import socket
import random
import threading
users = {}  
players = ""
f = open("words.txt", "r")
words = f.read().split()
f.close()
class Hangman_Server:
 '''This is the server side code for the Hangman game.'''
 def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((IP,port))
            self.s.listen()
            while 1:
                conn, addr = self.s.accept()
                print("Connected by: " , addr)
                t1 = threading.Thread(target=self.start_game, args=(conn, addr))
                print(t1)
                t1.start()
 
 def start_game(self, conn, addr):
     data = conn.recv(1024).decode()
     if ('Start' in data): 
        details = data.split(" ")[1]
        print(details)
        if (details not in users):
            conn.send(("You are a new user. Only registered players are allowed to play the game. If you want to register type \'yes\' else type \'no\'").encode())
            ans = conn.recv(1024).decode()
            #print(ans)
            if (ans == 'no'):
                conn.close()
            secret_word = random.choice(words)
            users[details] = Player(secret_word)
            players = users[details]
            print(players)
        else:
            if(details in users):
                players = users[details]
                #conn.send(("Hi" + details.encode())
            while 1:
                secret_word = random.choice(words)
                if(secret_word not in players.wordlist):
                    players.wordlist.append(secret_word)
                    break 
        self.hangman(conn,secret_word, details, players)   
        conn.close()             
 
 def hangman(self, conn, secret_word, name, players):
      '''The actual game code where the above three functions are called
      in aparticular order to guess the secret word correctly'''
      print(secret_word)
      letters_guessed = []
      i = 8
      out = "Hi " + name + "\n"
      out += "Welcome to the game, Hangman!\n"
      out += "I am thinking of a word that is "+ str(len(secret_word)) + " letters long\n"
      out +="------------------------\n"
      conn.sendall(out.encode())
      #The loop runs 8 times as the guesses are 8
      while i > 0:
          out = ''
          out += 'You have '+ str(i) + ' guesses left\n'
          out += 'available letters '+ self.getavailable_letters(letters_guessed) + '\n' + 'Please guess a letter: '
          conn.send(out.encode())
          guessword = conn.recv(1024).decode()
          #The guess word is converted into lower case 
          guessword = guessword.lower()
          #If the guessed word is in secret word and not in letters guessed
          #the append it to letters guessed
          try:
              guess = ''
              if 97<=ord(guessword)<=122:
                  if guessword in secret_word and guessword not in letters_guessed:
                      letters_guessed.append(guessword)
                      guess += "good guess : " + self.users_guess(secret_word, letters_guessed) + "\n"
                  #If the guessed word is in letters guessed then print that you have 
                  #already guessed the word   
                  elif guessword in letters_guessed:
                      guess += "Oops! You have already guessed that letter "+ self.users_guess(secret_word, letters_guessed) + '\n'    
                   # if secret word is not in secret word and not in lettersguessed then 
                   #decrement the number of guesses and append it to letters guessed     
                  else:
                      i = i-1
                      letters_guessed.append(guessword)
                      guess += "Oops! the letter is not in my word: " + self.users_guess(secret_word, letters_guessed) + '\n'
                  guess += '---------------------\n'
                  #If the secret word is guessed correctly then print you won
                  # else print you ran out of guesses and print the guess word.
                  if self.is_word_guessed(secret_word, letters_guessed):
                      guess += "Congratulations, you won!\n"
                      guess += "Your score is " + str(self.Score(secret_word, i))
                      players.score = self.Score(secret_word, i)
                      conn.sendall(guess.encode())
                      break
                  elif i == 0:
                      guess += "Sorry you ran out of guesses. The word was "+ secret_word + "\n"
                      guess += "Your score is 0"
                  conn.sendall(guess.encode())      
              else:
                  guess += "please enter an alphabet\n"
                  guess +='---------------------\n'
                  conn.sendall(guess.encode())
          except TypeError:
             conn.sendall(("please enter only single alphabet\n" + '---------------------\n').encode())
      lb = conn.recv(1024).decode()
      #print(lb)
      if (lb == 'Y'):
          x = self.LeaderBoard()
          conn.send(x.encode())
      else:
          conn.send(("Game Over").encode())


 def is_word_guessed(self, secret_word, letters_guessed):
    '''Expected Input: a string and a list of guessed words
    The function mainly checks if we guessed secret word or not.
    If the word is correct , then it returns True else returns False'''
    count = 0
    #The count of letters guessed correctly is calculated in the loop 
    for char in secret_word:
        if char in letters_guessed:
            count += 1
    if count == len(secret_word):
      return True
    else:
      return False

 @classmethod
 def users_guess(self, secret_word, letters_guessed):
    '''Expected Input:a string and a list of guessed words.
    This function returns a string which contains correctly guessed
    letters at their respective positions '''
    word = []
    #'_' is appended to the word list each time the loop runs.
    #The length of the word list is equal to secret word.
    for iteration in range(len(secret_word)):
        word.append('_')
    #If the letter is guessed correctly then it is returned with its position 
    #in the secret_word     
    for letter in letters_guessed:
        if letter in secret_word:
            for i, j in enumerate(secret_word):
                if letter == j:
                    word[i] = letter
    return " ".join(word)


 def getavailable_letters(self, letters_guessed):
    '''Expected input: a list of letters guessed by the user.
    This function mainly returns a string which contains the letters,
    other than the letters that are not present in the secret_word but
     guessed by the user, in the alphabetical order'''
    lis = ''
    import string
    string = string.ascii_lowercase
    # If the letter is guessed then it is deleted from the list of available letters
    for i in string:
        if i not in letters_guessed:
            lis = lis+i
    if lis == '':
        lis = string
    return lis

 @classmethod
 def LeaderBoard(self):
     #print(users)
     board = sorted(users.items(), key=lambda player: (player[1].score, player[0]), reverse = True)
     out = ""
     for i in board:
         out +=  i[0] + "\t" + str(i[1].score) + "\n"
     return out

 @classmethod
 def Score(self, secret_word, n):
     return len(secret_word) * n

class Player:
    score = 0
    wordlist = []
    '''The class is player class whihc consists of score and wordlist of a player'''
    def __init__(self,Secretword):
        super().__init__()
        self.wordlist.append(Secretword)

def main():
   Hangman_Server('127.0.0.1', 2525)

if __name__ == "__main__":
    main()              
