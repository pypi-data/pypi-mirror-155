# 2022.6.16
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(layout='wide')
from common import * 

st.sidebar.header( hget(f"config:rid-{rid}", "title","i+1 写作智慧课堂") )
st.sidebar.caption(uid.split(',')[-1])

keys = redis.r.keys('config:plusone-teacher:*') #arr = redis.r.hgetall("config:plusone:admin") # title -> url 
item = st.sidebar.radio('', [k.split(':')[-1] for k in keys]) 

st.sidebar.markdown('''---''') 
url  = hget(f'config:plusone-teacher:{item}', 'url')
tags = { k : st.sidebar.radio(hget('config:plusone:settings',k,k),  json.loads(hget(f'config:plusone-teacher:{item}', k)) ) for k in redis.r.hkeys(f'config:plusone-teacher:{item}') if k.startswith('var-')}
if tags:
	for k,v in tags.items(): # {radio-sid: 4}
		url = url.replace(f"${k}", str(v)) 
components.iframe( url ,  height = 1200) #width=1500,