from PIL import Image
import os

# Создаем новую директорию для сохранения файлов JPEG
if not os.path.exists('jpeg'):
    os.makedirs('jpeg')

# Проходимся по всем файлам с расширением .heic
for filename in os.listdir('C:/1tomh/'):
    if filename.endswith('.heic'):
        with Image.open(os.path.join('C:/1tomh/', filename)) as im:
            # ...
            # Получаем путь для нового файла JPEG
            new_filename = os.path.join('jpeg', os.path.splitext(filename)[0] + '.jpeg')
            # Сохраняем изображение в формате JPEG
            im.convert('RGB').save(new_filename)
