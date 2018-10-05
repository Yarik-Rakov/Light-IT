import time
from random import shuffle

class Koloda:

# Начальные данные
	def __init__(self,
				cards = [6,7,8,9,10,11,12,13,14], # достоинство карт в числовом виде
				masti = {"pika": " Пика", "kresta": " Креста", "bubna": " Бубна", "cherva": " Черва"},
				name = {"valet": "Валет", "dama": "Дама", "korol": "Король", "tuz": "Туз"}, # достоинство карт в строковом виде для карт с достоинством выше 10
				cards_num = 6, # кол-во карт в наборе
				players = input("\nВведите количество игроков от 2 до 6: "), # ввод количество игроков
				kozir_count = []): # количество козырных карт
		
		self.cards = cards
		self.masti = masti
		self.name = name
		self.players = players
		self.cards_num = cards_num
		self.kozir_count = kozir_count

# Вводим количество игроков
	def players_num(self):

		# проверяем, является ли ввод числом и оно в диапазоне от 2 до 6
		while not str(self.players).isnumeric() or int(self.players) < 2 or int(self.players) > 6:
			self.players = input("\nВведите количество игроков от 2 до 6: ")
		print("\nКол-во игроков:", self.players + "\n")
		return self.players

# Создаём колоду
	def koloda(self):
		self.players_num()
		koloda = []
		for i in self.cards:
			for j in self.masti:
				koloda.append(str(i) + self.masti[j])
		shuffle(koloda) # перетасовываем колоду
		return koloda

# Выдаём карты на руки, выкладываем козырь и получаем количество козырных карт для каждого выданного набора
	def vidacha(self):
		arr = self.koloda()
		arr_vidano = []
		self.players = int(self.players)

		# получаем козырную карту (следующая карта после раздачи для 2-5 игроков или последняя карта в колоде для 6 игроков)
		if self.players == 6:
			kozir_card = arr[self.players * self.cards_num - 1]		
		else:
			kozir_card = arr[self.players * self.cards_num] 	
		
		kozir_card_arr = kozir_card.split()
		kozir_card_mast = kozir_card_arr.pop(1) # выводим масть козырной карты

		all_indexes = []
		for i in range(0, self.players):

			# получаем наборы из 6-ти карт для n-ного кол-ва игроков из верха колоды
			arr_vidano.append(arr[i * self.cards_num: (i+1) * self.cards_num]) 
			nabor_igrok = "Набор карт для "+ str(i+1)+ "-го игрока: " 

			# меняем достоинство карты с числа на имя и выводим наборы на экран
			nabor = str(arr_vidano[i]).replace("11", "Валет").replace("12", "Дама").replace("13", "Король").replace("14", "Туз").replace("'","")[1:-1] 
			print(nabor_igrok + nabor)

			# получаем индексы козыря и сохраняем их в массив arr_indexes
			arr_indexes = []	
			for j in arr_vidano[i]:
				if kozir_card_mast in j:
					a = arr_indexes.append(arr_vidano[i].index(j))
			
			# сохраняем массив arr_indexes в массив all_indexes, тем самым образуя массив второго порядка
			all_indexes.append(arr_indexes) 
	
		# сохраняем кол-во козырных карт в массив kozir_count
		for i in all_indexes:
			self.kozir_count.append(len(i))

		# выводим козырную карту на экран
		print("\nКозырь: " + kozir_card_mast + "\n") 
		return arr_vidano

	# Считаем рейтинг (старшинство) достоинств
	def rating(self):

		# массив arr будет преобразован из набора карт с мастями в массив только с их числовыми достоинствами
		arr = self.vidacha() 

		# делаем копию массива с наборами карт для дальнейшего вывода их на экран в "Старших наборах"
		nabor = arr.copy()
		
		# сохраняем количество козырей в массив new_priority, 
		# где первый элемент с количеством козырей будет рассчитываться для первого набора карт в подсчете рейтинга
		new_priority = self.kozir_count

		# образуем числовую силу козыря
		# умножаем количество козырей каждого элемента массива new_priority на 9 для образования числовой силы козыря,
		# чтобы позже прибавить элементы (числовые силы козыря) к сумме достоинств без числовой силы козыря 
		new_priority = [item * 9 for item in new_priority] 

		highest_set = []
		for i in range(0, self.players):

			# убираем из набора карт в массиве arr масти
			arr[i] = str(arr[i])[1:-1].replace(self.masti["pika"], "").replace(self.masti["kresta"], "").replace(self.masti["bubna"], "").replace(self.masti["cherva"], "").replace("'","").replace(",","").split()
			
			# конвертируем каждый элемент массива arr (каждое достоинство карты) в тип integer
			arr[i] = [int(item) for item in arr[i]]

			# суммируем элементы (достоинства карты) без учета числовой силы козыря
			sum_arr = sum(arr[i])

			# суммируем сумму достоинств карт с числовой силой козыря
			k = sum_arr + new_priority[i]

			# сохраняем суммирование суммы достоинств карт с числовой силой козыря для каждого набора в массив highest_set для дальнейших расчетов
			highest_set.append(k)

		# находим максимальную сумму достоинств карт среди всех сумм достоинств карт каждого набора
		winner_num = max(highest_set)

		# будем вычислять индексы с максимальными суммами достоинств карт и сохранять их в массив winner_sets
		winner_sets = []
		for i in highest_set:
			for j in highest_set:
				if str(winner_num) in str(j):

					# сохраняем индекс первой максимальной суммы достоинств в переменную winner_index
					winner_index = highest_set.index(winner_num)

					# меняем индекс первой максимальной суммы достоинств карт на 0,
					# чтобы при следующей итерации получить индекс следующей максимальной суммы достоинств карт, если таковая существует
					highest_set[winner_index] = 0 

					# сохраняем индексы с максимальными суммами достоинств карт (номеров игроков) в массив winner_sets
					winner_sets.append(winner_index+1)

		# выводим на экран номера игроков со старшими картами			
		print("Старший набор карт у игрока(ов) под номером(ами):",str(winner_sets)[1:-1]+"\n")

		# меняем численное представление достоинств карт обратно на именные и выводим на экран
		for i in winner_sets:
			print("Старший набор:",str(nabor[i-1])[1:-1].replace("'","").replace("11", "Валет").replace("12", "Дама").replace("13", "Король").replace("14", "Туз"))
		
		# задержка перед выходом из программы
		return time.sleep(3000)

# создаём объект k класса Koloda
k = Koloda()

# вызываем метод rating() класса Koloda через его объект k (запускаем игру)
k.rating()


