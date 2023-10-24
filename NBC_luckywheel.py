import streamlit as st
import pandas as pd
import time
import datetime
import requests
from web3 import Web3
import tweepy
import brotli
import json
import base64
import time

def time_difference(timestamp_str):
    # Parse the timestamp string into a datetime object
    timestamp_datetime = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
    
    # Get the current UTC time
    current_time = datetime.datetime.utcnow()
    
    # Calculate the difference
    delta = timestamp_datetime- current_time
    if delta.total_seconds() < 0:
        return "Finished"
    
    # Extract days, hours, minutes, and seconds from the timedelta object
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return minutes, seconds


NBC_Barear = st.secrets["NBC_Barear"]


def get_latest_nbc_tweet():
	# Endpoint URL
	url = "https://alpha-api.newbitcoincity.com/api/tweet/list"

	# Query parameters
	params = {
	    "network": "nos",
	    "version": "2",
	    "page": "1",
	    "limit": "500",
	    "address": "0x58264Ac8e24a101ef90b28616C740863b159083b",
	    "only_following": "true"
	}

	# Headers
	headers = {
	    "Accept": "application/json, text/plain, */*",
	    "Accept-Encoding": "gzip, deflate, br",
	    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
	    "Authorization": f"Bearer {NBC_Barear}",
	    "Origin": "https://pro.newbitcoincity.com",
	    "Referer": "https://pro.newbitcoincity.com/",
	    "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
	    "Sec-Ch-Ua-Mobile": "?0",
	    "Sec-Ch-Ua-Platform": "Windows",
	    "Sec-Fetch-Dest": "empty",
	    "Sec-Fetch-Mode": "cors",
	    "Sec-Fetch-Site": "same-site",
	    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
	}

	# Making the GET request
	response = requests.get(url, headers=headers, params=params)

	# Parsing the JSON response
	data = response.json()
	result_list = []

	for i in data["result"]:
	    if i["content"] == "Open a Lucky Wheel":
	        try:
	            mins, sec = time_difference(i["prize_wheel_event"]["ExpiredAt"])
	            expir_str = f"{mins} mins, {sec} sec"
	        except:
	            expir_str = "Finished"
	        entry = {
	            "img_url": i["prize_wheel_event"]["Twitter"]["TwitterAvatar"],
	            "user_name": i["prize_wheel_event"]["Twitter"]["TwitterUsername"],
	            "user_address": i["prize_wheel_event"]["TwitterAddress"],
	            "expir_date": f"{expir_str}",
	            "status": i["prize_wheel_event"]["Status"],
	            "is_holder": i["prize_wheel_event"]["IsHolder"],
	            "price": i["prize_wheel_event"]["Amount"]
	        }
	        result_list.append(entry)

	return result_list

# st.set_page_config(layout="wide")

def image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

icon_url = f"data:image/png;base64,{image_to_base64('./SocialFi_Tracker.png')}"
title_text = "NewBitcoinCity Lucky Wheel Sniper"

st.markdown(f'<img src="{icon_url}" style="vertical-align:middle; display:inline; margin-right:10px; width:40px; height:40px;"> <span style="font-size: 30px; vertical-align:middle;"><strong>{title_text}</strong></span>', unsafe_allow_html=True)


# st.title("NewBitcoinCity Lucky Wheel Sniper")

current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
st.write("Last updated:", current_time)
st.write("Produced by 0x0funky: ", "https://twitter.com/0x0funky ","FT:" "https://friend.tech/0x0funky")
st.write("SocialFi-Tracker (Eazy to find infomation across SocialFi): ", "https://socialfi-tracker.streamlit.app/")


# List to store fetched datas
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
		st.markdown(f"""
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
    Profile
</div>
""", unsafe_allow_html=True)
with col2:
		st.markdown(f"""
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
    Follow Now
</div>
""", unsafe_allow_html=True)
with col3:
		st.markdown(f"""
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
    Price
</div>
""", unsafe_allow_html=True)
with col4:
		st.markdown(f"""
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
    Need Key
</div>
""", unsafe_allow_html=True)
with col5:
		st.markdown(f"""
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
    Status
</div>
""", unsafe_allow_html=True)
with col6:
	st.markdown(f"""
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
    Need Key
</div>
""", unsafe_allow_html=True)
# if st.button("Start Fetching Data"):
with st.empty():
    while True:
        new_data = get_latest_nbc_tweet()
        # st.session_state.data_list.insert(0, new_data)  # insert new data at the top
            
        # If data_list exceeds 15 rows, remove the oldest row
        # if len(st.session_state.data_list) > 15:
            # st.session_state.data_list.pop(-1)
        new_data = new_data[:15]
        # Displaying the data
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            for data in new_data:
                st.markdown(f"""
<div style='text-align: center; margin-bottom: 16px;'>
    <img src="{data['img_url']}" width="50"/>
</div>
""", unsafe_allow_html=True)
        with col2:
            for data in new_data:
                address_url = "https://pro.newbitcoincity.com/alpha/profile/"+data["user_address"]
                # st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>{data['expir_date']}</div>", unsafe_allow_html=True)
                st.markdown(f"""
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>
    <a href="{address_url}" target="_blank">{data['user_name']}</a>
</div>
""", unsafe_allow_html=True)
        	    
            	# st.text(data['status'])
        with col3:
            for data in new_data:
                st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>{data['price']} BTC</div>", unsafe_allow_html=True)
        with col4:
            for data in new_data:
        	    st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>{data['expir_date']}</div>", unsafe_allow_html=True)
            	# st.text(data['value'])
        with col5:
            for data in new_data:
            	if data['status'] == "running":
            		st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: green; color: white;'>{data['status'].upper()}</div>", unsafe_allow_html=True)
            	else:
            		st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: red; color: white;'>{data['status'].upper()}</div>", unsafe_allow_html=True)
        	    # st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>{data['status'].upper()}</div>", unsafe_allow_html=True)
            	# st.text(data['counts'])
        with col6:
            for data in new_data:
            	is_holder = "Yes" if data['is_holder'] else "No"
            	if is_holder == "Yes":
            		st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>{is_holder}</div>", unsafe_allow_html=True)
            	else:
            		st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: green; color: white;'>{is_holder}</div>", unsafe_allow_html=True)
            	# st.text(data['token'])

        
        time.sleep(2)

        # st.write("Produced by 0x0funky: ", "https://twitter.com/0x0funky ")
        # st.write("FT: ", "https://friend.tech/0x0funky")
        # st.write("SocialFi Tracker open for free now, will open for key holders only in the future.")