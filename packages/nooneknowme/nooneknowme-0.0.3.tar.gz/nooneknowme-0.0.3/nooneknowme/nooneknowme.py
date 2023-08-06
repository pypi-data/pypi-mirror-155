from csv import DictReader
import random
class Nooneknowme :
    # คลาส ข้อมูลเกี่ยวกับข้อมูลที่เมคขึ้นมา
    def __init__(self):
        self.name = 'Noone'
        self.hobby = 'Archering'
        self.music = 'https://youtu.be/eu1auaUHy0c'

    def show_name(self):
        print(f'Hi, I am {self.name}')

    def playmusic(self):
        print('https://youtu.be/eu1auaUHy0c')

    def about(self):
        text = """
-----------------------------------
It's just me and me and me me me!!!
-----------------------------------

        """
        print(text)

    def picasciiart(self):
        picart = """
   ________________
  |   |,"    `.|   | 
  |  I love myself |
  |O _\   />   /_  |   ___ _
  |_(_)'.____.'(_)_|  (")__(")
  [___|[=]__[=]|___]  //    \\


        """
        print(picart)
    
    def dice2(self):
        dice_list = [1,2,3,4,5,6]
        firstdice = random.choice(dice_list)
        secounddice = random.choice(dice_list)
        print(f'ทอยเต๋าได้: {firstdice} ,{secounddice}')

        


if __name__ == '__main__':
    testname = Nooneknowme()
    testname.show_name()
    testname.about()
    testname.picasciiart()
    testname.playmusic()
    testname.dice2()