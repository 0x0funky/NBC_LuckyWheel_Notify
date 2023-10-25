import streamlit as st
import time
import datetime
import requests
import json
import base64

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
        "Authorization": f"Bearer {NBC_Barear}",
    }

    # Making the GET request
    response = requests.get(url, headers=headers, params=params)

    # Parsing the JSON response
    data = response.json()
    result_list = []

    def get_access_key_number(wheel_address):
        url = f"https://alpha-api.newbitcoincity.com/api/player-share/profile?network=nos&address={wheel_address}"
        response = requests.get(url, headers=headers)
        data = response.json()
        return data["result"]["min_holding_requirement"]

    for i in data["result"]:
        if i["content"] == "Open a Lucky Wheel":
            try:
                mins, sec = time_difference(i["prize_wheel_event"]["ExpiredAt"])
                expir_str = f"{mins} m, {sec} s"
            except:
                expir_str = "Finished"
            if i["prize_wheel_event"]["Status"] == "running":
                if i["prize_wheel_event"]["IsHolder"]:
                    address = i["prize_wheel_event"]["TwitterAddress"]
                    amount_access = get_access_key_number(address)
                else:
                    amount_access = 0
                winner_avat = ""
                winner_username = "???"
                winner_address = "???"
            else:
                if i["prize_wheel_event"]["IsHolder"]:
                    amount_access = i["prize_wheel_event"]["PrizeWheelSpend"]["Token"]["MinHoldingRequirement"]
                else:
                    amount_access = 0
                winner_avat = i["prize_wheel_event"]["PrizeWheelSpend"]["ToTwitter"]['TwitterAvatar']
                winner_username = i["prize_wheel_event"]["PrizeWheelSpend"]["ToTwitter"]['TwitterUsername']
                winner_address = i["prize_wheel_event"]["PrizeWheelSpend"]["ToTwitter"]['AddressChecked']
            entry = {
                "img_url": i["prize_wheel_event"]["Twitter"]["TwitterAvatar"],
                "user_name": i["prize_wheel_event"]["Twitter"]["TwitterUsername"],
                "user_address": i["prize_wheel_event"]["TwitterAddress"],
                "expir_date": f"{expir_str}",
                "status": i["prize_wheel_event"]["Status"],
                "is_holder": amount_access,
                "price": i["prize_wheel_event"]["Amount"],
                "winner_url" : winner_avat,
                "winner_username" : winner_username,
                "winner_address" : winner_address
            }
            result_list.append(entry)

    return result_list

def main_content():
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
            st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
        Profile
    </div>
    """, unsafe_allow_html=True)
    with col2:
            st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
        Follow
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
        Time
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
        KeyNeed
    </div>
    """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: blue; color: white;'>
        Winner
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
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            
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
    <div style='text-align: center; margin-bottom: 30px; margin-top: 10px; margin-left: -10px;'>
        <a href="{address_url}" target="_blank">{data['user_name']}</a>
    </div>
    """, unsafe_allow_html=True)
                    
                    # st.text(data['status'])
            with col3:
                for data in new_data:
                    st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;white-space: nowrap;'>{data['price']} BTC</div>", unsafe_allow_html=True)
            with col4:
                for data in new_data:
                    st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;white-space: nowrap;'>{data['expir_date']}</div>", unsafe_allow_html=True)
                    # st.text(data['value'])
            with col5:
                for data in new_data:
                    if data['status'] == "running":
                        st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: green; color: white;white-space: nowrap;'>{data['status'].upper()}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; background-color: red; color: white;white-space: nowrap;'>{data['status'].upper()}</div>", unsafe_allow_html=True)
                    # st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>{data['status'].upper()}</div>", unsafe_allow_html=True)
                    # st.text(data['counts'])
            with col6:
                for data in new_data:
                    # is_holder = "Yes" if data['is_holder'] else "No"
                    if data['is_holder'] != 0:
                        st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; white-space: nowrap;'>{data['is_holder']} Keys</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; white-space: nowrap;  background-color: green; color: white;'> FREE </div>", unsafe_allow_html=True)
                    # st.text(data['token'])
            with col7:
                for data in new_data:
                    if data['winner_url'] == "":
                        st.markdown(f"<div style='text-align: center; margin-bottom: 30px; margin-top: 10px; white-space: nowrap;'> ???? </div>", unsafe_allow_html=True)
                    else:
                        winner_url = "https://pro.newbitcoincity.com/alpha/profile/"+data["winner_address"]
                        st.markdown(f"""
    <a href="{winner_url}" target="_blank" style="text-decoration: none; color: inherit;">
        <div style='text-align: center; margin-bottom: -5px;'>
            <img src="{data['winner_url']}" width="40px"/>
            <p style="font-size: 10px; margin-bottom: 10px; white-space: nowrap;">{data["winner_username"]}</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

            
            time.sleep(2)

        # st.write("Produced by 0x0funky: ", "https://twitter.com/0x0funky ")
        # st.write("FT: ", "https://friend.tech/0x0funky")
        # st.write("SocialFi Tracker open for free now, will open for key holders only in the future.")

# st.set_page_config(layout="wide")
st.set_page_config(page_title= "SocialFi-Tracker", page_icon="./SocialFi_Tracker.png")

def image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

icon_url = f"data:image/png;base64,{image_to_base64('./SocialFi_Tracker.png')}"
title_text = "NewBitcoinCity Lucky Wheel Sniper"

st.markdown(f'<img src="{icon_url}" style="vertical-align:middle; display:inline; margin-right:10px; width:40px; height:40px;"> <span style="font-size: 30px; vertical-align:middle;"><strong>{title_text}</strong></span>', unsafe_allow_html=True)


# st.title("NewBitcoinCity Lucky Wheel Sniper")

current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
st.write("Last updated:", current_time)

st.markdown(f"""
    <div>
        Produced by <a href="https://twitter.com/0x0funky" target="_blank">0xFunky</a>
    </div>
    """, unsafe_allow_html=True)

st.write("SocialFi-Tracker (Eazy to find information across SocialFi): ", "https://socialfi-tracker.streamlit.app/")

st.write('''
<style>
@media (max-width: 600px) {
    [data-testid="block-container"] {
        flex-direction: row !important;
    }
    [data-testid="column"] {
        width: 10% !important;  /* 100% divided by 6 columns */
        flex: 0 0 10% !important;
        min-width: 10% !important;
        font-size: 10px;
    }
    [data-testid="column"] img {
        width: 30px !important;
        height: auto;  /* This ensures the aspect ratio of the image remains unchanged */
        margin-bottom: 10px;
    }
    [data-testid="column"] p {
        font-size: 8px;
        margin-top:-10px;
        margin-bottom: -10px;
        margin-left:-5px;
    }
}
</style>
''', unsafe_allow_html=True)

ACCESS_KEY = "nbcfunkyonly"

user_input_key = st.text_input("Enter the access key: (Find key in FT room or NBC circle)")


if user_input_key == ACCESS_KEY:
    main_content()
else:
    if user_input_key:
        print ("========== You Press the Wrong Key!! ===========")
        st.write("Incorrect key! Join 0xFunky FT room or NBC circle to get the key!")
        st.write("FT:", "https://friend.tech/0x0funky")
        st.write("NBC:", "https://pro.newbitcoincity.com/alpha/profile/0x58264ac8e24a101ef90b28616c740863b159083b")


# custom_css = """
# <style>
#     @media (max-width: 600px) {
#         div[data-testid="column"] > div:first-of-type {
#             flex-basis: 100% !important; 
#         }
#     }
# </style>
# """
# st.markdown(custom_css, unsafe_allow_html=True)
# List to store fetched datas

