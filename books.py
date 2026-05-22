def add_book (books):
  str - 'Введите через пробел название, автор'
  while True:
    try:
      title, author - input(str).split()
    except:
      print('Повторите ввод')
    books. append({
      'title': title,
      'author': author
    })
    break
