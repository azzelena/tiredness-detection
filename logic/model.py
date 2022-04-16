# подключение библиотек
import cv2 
import os # для воспроизведения звука (mac only)
import geocoder
import random

# загрузка предобученных моделей в переменные
eye_cascPath = 'haarcascade_eye_tree_eyeglasses.xml'  # eye detect model
face_cascPath = 'haarcascade_frontalface_alt.xml'  # face detect model
# запись классификатора (глаза и лицо) в переменные
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + face_cascPath)
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + eye_cascPath)

# включение веб-камеры устройства
cap = cv2.VideoCapture(0)

# начальное значение счетчика времени закрытия глаза
time_track = 0

# флаг для определения - трасса или город
is_city = False


# функция для голосовых подсказок и предупреждений (macOS)
def say(msg = "Finish", voice = "Victoria"):
    os.system(f'say -v {voice} {msg}')

# geo
g = geocoder.ip('me')

if g.city != None:
    is_city = True
    print('Вы находитесь в черте города ', g.city, ',' , g.country)
    print(is_city)
else:
    print('Вы находитесь не в населенном пункте')
    print(is_city)
    
# logic   
while True:
    # считывание изображения с видео
    ret, img = cap.read()
    if ret:
        # отображение фрейма с видео с отображение в цветах
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # поиск лиц на видео
        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(10, 10),
        )
        if len(faces) > 0:
            # если лица найдены, приближаем их и обводим "в круг" для дальнейшей детекции глаз
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
            frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
            # детекция глаз на видео
            eyes = eyeCascade.detectMultiScale(
                frame,
                scaleFactor=1.1, # на сколько уменьшается изображение
                minNeighbors=5, # минимальное число соседей для детекции
                minSize=(30, 30),
            )
            # проверка - есть ли открытые глаза на видео (ветка "нет")
            
            # имитация для фиксирования скорости
            speed = random.randint(40, 160)

            if len(eyes) == 0:
                print('Глаза закрылись!!!')
                time_track+=1
                print('прошло' , time_track, ' секунд')
                # если глаза закрыты > 3 секунд
                if (time_track == 3) & (is_city == True):
                    print('Первое предупреждение')
                    print('Ваша скорость: ', speed, ' км/ч')
                    if speed > 60:
                        print('Недалеко от вас есть кафе. Выпейте кофе')
                    
                    say('Its not a good time for sleeping!')
            
                elif (time_track == 3) & (is_city == False):
                    if speed > 110:
                        print('Кажется, вы устали. Найдите ночлег')
                    
                    say('Its not a good time for sleeping!')
                    
                # если глаза закрыты >= 6 секунд
                if time_track >= 6:
                    print('Всё! Уснул!!')
                    
                    say('Wake up man! You are in danger!')
                    
            # проверка - есть ли открытые глаза на видео (ветка "есть")
            else:
                time_track=0
                print('Глаза открыты!!!')
            frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)
            cv2.imshow('Распознование лица', frame_tmp)
        # проверка происходит каждую секунду 
        waitkey = cv2.waitKey(1)
        if waitkey == ord('q') or waitkey == ord('Q'):
            cv2.destroyAllWindows()
            break
