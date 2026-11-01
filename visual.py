import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from PIL import Image
import numpy as np
import time
import cv2

st.set_page_config(layout="wide") 
st.title('Traffic Violation Detecting')

actions = 'Video Processing', 'Read Offenders', 'Show Image Offender'

select = st.selectbox('Select an action', list(actions))
with st.form('Optional Data'):
    if select == 'Video Processing':
        video = st.text_input('Video path', value = 'data/Traffic_IP_Camera_video.mp4')
        st.markdown('Default Value Automatically Inserted')
        config = st.text_input('Config Path',  value = 'data/config.yaml')
        st.markdown('Default Value Automatically Inserted')

        if st.form_submit_button('Execute'):
            
            frame_empty = st.empty()
            putdata = {
                'file_path' : video,
                'config_path' : config}
            
            response =  requests.post('http://127.0.0.1:8000/video_process', json=putdata)
            if response.status_code == 200:
                st.success('Start process')
                with st.expander('Logs...'):
                    log_box = st.empty()
                    while True:
                        try:
                            log = requests.get('http://127.0.0.1:8000/logs/')
                            if log.status_code == 200:
                                log_text = log.text.replace('\\n', '\n')
                                log_box.code(log_text, language='text', height=300)
                                    
                                if 'Video stream ended' in log_text:
                                    st.success('Process ended')
                                    break
                                
                        except Exception:
                            pass
                        
                        time.sleep(0.5)
                
                    
    elif select == 'Read Offenders':
        config = st.text_input('Config Path', value = 'data/config.yaml')
        st.markdown('Default Value Automatically Inserted')
        
        if st.form_submit_button('Execute'):
            response = requests.get('http://127.0.0.1:8000/offenders/')
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                st.table(df.style.hide(axis='index'))
        
    else:
        id = st.text_input('Offender ID')
        
        if st.form_submit_button('Execute'):
            response = requests.get(f'http://127.0.0.1:8000/offenders/{id}/image/')
            if response.status_code == 200:
                imageby = BytesIO(response.content)
                image = Image.open(imageby)
                st.image(image)
            
            else:
                st.error('Not Found')