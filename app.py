import streamlit as st # фреймворк для запуска приложения
import geocoder # библиотека для определения геопозиции
import pandas as pd # библиотека для создания фрейма с широтой и долготой

# флаг для определения - трасса или город
is_city = False

# Title
st.title('Детекция усталости водителя')

st.write(' ')


# geo
g = geocoder.ip('me')
if g.city != None:
    is_city = True
    st.write(' ### Вы находитесь в черте города ', g.city, ',' , g.country)
else:
    st.write(' ### Вы находитесь не в населенном пункте')

df = pd.DataFrame({'lat': [g.latlng[0]], 'lon': [g.latlng[1]]})

st.map(df)

video_file = open('example.mov', 'rb')
video_bytes = video_file.read()

st.write(' ')
st.write('### Видеоиллюстрация работы программы')

st.video(video_bytes)
