import threading
import random
from queue import Queue
import time


class Table: #  стол, хранит информацию о находящемся за ним гостем (Guest)
    def __init__(self, number):
        self.number = number
        self.guest = None




class Guest(threading.Thread): # Создаём класс "Гости"
    def __init__(self, name):
        super().__init__()
        self.name = name


    def run(self):
        time_ = random.randint(3, 10) # гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
        time.sleep(time_)




class Cafe: # кафе, в котором есть определённое кол-во столов и
    # происходит имитация прибытия гостей (guest_arrival) и их обслуживания (discuss_guests).
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables


    def guest_arrival(self, *guests):
        for guest in guests: # добавляем в очередь гостей
            allocated = False #проверяем, есть ли гости в очереди
            for table in self.tables: #перебираем все столы в очереди
                if table.guest is None: # если стол свободен
                    table.guest = guest  #сажаем гостя за стол
                    guest.start() # запускаем гостя в отдельном потоке
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    allocated = True # стол свободен
                    break


            if not allocated:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")


    def discuss_guests(self):
        while (not self.queue.empty() #проверяет пуст ли стек (тип структуры данных,который следует принципу
        #"Первый вошел - первый вышел") или нет.
               or any(table.guest is not None for table in self.tables)): # проверка на пустые столы
            for table in self.tables:
                if table.guest is not None: # если стол свободен
                    if not table.guest.is_alive(): # проверка состояния потока guest в очереди и его завершения работы в очереди
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None


                        if not self.queue.empty(): # если есть еще столы, то выбираем следующий стол из очереди
                            next_guest = self.queue.get() # получаем следующий стол из очереди
                            table.guest = next_guest # устанавливаем нового стола в очереди
                            next_guest.start() # запускаем поток guest в очереди
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            time.sleep(1)  # небольшая пауза, чтобы избежать интенсивного цикла



tables = [Table(number) for number in range(1, 6)]
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman','Vitoria', 'Nikita', 'Galina', 'Pavel',
                'Ilya', 'Alexandra']
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()








'''
#Необходимо имитировать ситуацию с посещением гостями кафе.
#Создайте 3 класса: Table, Guest и Cafe.
#Класс Table:
#Объекты этого класса должны создаваться следующим способом - Table(1)
#Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)
#Класс Guest:
#Должен наследоваться от класса Thread (быть потоком).
#Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
#Обладать атрибутом name - имя гостя.
#Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
#Класс Cafe:#
#Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
#Обладать атрибутами queue - очередь (объект класса Queue) и
# tables - столы в этом кафе (любая коллекция).
#Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).
#Метод guest_arrival(self, *guests):
#Должен принимать неограниченное кол-во гостей (объектов класса Guest).
#Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest),
# запускать поток гостя и выводить на экран строку
# "<имя гостя> сел(-а) за стол номер <номер стола>".
#Если же свободных столов для посадки не осталось, то помещать гостя в очередь
# queue и выводить сообщение "<имя гостя> в очереди".
#Метод discuss_guests(self):
#Этот метод имитирует процесс обслуживания гостей.
#Обслуживание должно происходить пока очередь не пустая (метод empty)
# или хотя бы
# один стол занят.
#Если за столом есть гость(поток) и гость(поток) закончил приём пищи
# (поток завершил
# работу - метод is_alive), то вывести строки "<имя гостя за текущим столом>
# покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен". Так же
# текущий стол освобождается (table.guest = None).
#Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None),
# то текущему столу присваивается гость взятый из очереди (queue.get()).
# Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а)
# за стол номер <номер стола>"
#Далее запустить поток этого гостя (start)
#Таким образом мы получаем 3 класса на основе которых имитируется работа кафе:
#Table - стол, хранит информацию о находящемся за ним гостем (Guest).
#Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
#Cafe - кафе, в котором есть определённое кол-во столов и происходит имитация
# прибытия гостей (guest_arrival) и их обслуживания (discuss_guests).#
#Примечания:
#Для проверки значения на None используйте оператор is (table.guest is None).
#Для добавления в очередь используйте метод put, для взятия - get.
#Для проверки пустоты очереди используйте метод empty.
#Для проверки выполнения потока в текущий момент используйте метод is_alive.#
##Выполняемый код:
#class Table:
#...
#class Guest:
#...
#class Cafe:
#...
# Создание столов
#tables = [Table(number) for number in range(1, 6)]
# Имена гостей
#guests_names = [
#'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
#'#Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
#]
# Создание гостей
#guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
#cafe = Cafe(*tables)
# Приём гостей
#cafe.guest_arrival(*guests)
# Обслуживание гостей
#cafe.discuss_guests()
'''