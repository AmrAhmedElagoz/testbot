import streamlit as st
from streamlit_chat import message as st_message
from transformers import pipeline
import random
import string
# import SessionState


# @st.experimental_singleton
@st.cache(allow_output_mutation=True)
def load_model():
    model = pipeline('question-answering',model='ZeyadAhmed/AraElectra-Arabic-SQuADv2-QA')
    return model
qa = load_model()


if 'count' not in st.session_state:
	st.session_state.count = 0

head = st.text_input("enter the topic name")
context= st.text_area("please enter your topic")

@st.experimental_singleton
def callback():
    # button_state= st.session_state["button"]
    head = st.text_input("enter the topic name", key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
    context= st.text_area("please enter your topic", key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))



st.button('add new context', on_click= callback)

# if add:
#     st.session_state.count += 1

# for i in range(st.session_state.count):
#     head = st.text_input("enter the topic name", key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
#     context= st.text_area("please enter your topic", key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
# if st.button('add new context', key = 'button'):
    # st.session_state.count += 1
    # if st.session_state.count > 1:
    #     for i in range(st.session_state.count - 1):
    #         head = st.text_input("enter the topic name", key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
    #         context= st.text_area("please enter your topic", key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))



if "history" not in st.session_state:
    st.session_state.history = []




def generate_answer():
    user_message = st.session_state.input_text
    # inputs = tokenizer(st.session_state.input_text, return_tensors="pt")
    # result = model.generate(**inputs)

    try:
        message_bot = qa(question= user_message, context= context)
        print(message_bot)

        if message_bot['score'] <= 0.2:
            message_bot = "sorry i didn't get that"
            st.session_state.history.append({"message": user_message, "is_user": True})
            st.session_state.history.append({"message": message_bot, "is_user": False})
            st.session_state.input_text = ""
            
        else:    
            st.session_state.history.append({"message": user_message, "is_user": True})
            st.session_state.history.append({"message": message_bot['answer'], "is_user": False})
            st.session_state.input_text = ""
            
                        
    except:
        print("Empty")



st.text_input("Talk to the bot", key="input_text",on_change = generate_answer)

count = 0
for chat in st.session_state.history:
    chat['key']=count
    count +=1
    st_message(**chat)  # unpacking
    

# """Hack to add per-session state to Streamlit.
# Usage
# -----
# >>> import SessionState
# >>>
# >>> session_state = SessionState.get(user_name='', favorite_color='black')
# >>> session_state.user_name
# ''
# >>> session_state.user_name = 'Mary'
# >>> session_state.favorite_color
# 'black'
# Since you set user_name above, next time your script runs this will be the
# result:
# >>> session_state = get(user_name='', favorite_color='black')
# >>> session_state.user_name
# 'Mary'
# """
# try:
#     import streamlit.ReportThread as ReportThread
#     from streamlit.server.Server import Server
# except Exception:
#     # Streamlit >= 0.65.0
#     import streamlit.report_thread as ReportThread
#     from streamlit.server.server import Server


# class SessionState(object):
#     def __init__(self, **kwargs):
#         """A new SessionState object.
#         Parameters
#         ----------
#         **kwargs : any
#             Default values for the session state.
#         Example
#         -------
#         >>> session_state = SessionState(user_name='', favorite_color='black')
#         >>> session_state.user_name = 'Mary'
#         ''
#         >>> session_state.favorite_color
#         'black'
#         """
#         for key, val in kwargs.items():
#             setattr(self, key, val)


# def get(**kwargs):
#     """Gets a SessionState object for the current session.
#     Creates a new object if necessary.
#     Parameters
#     ----------
#     **kwargs : any
#         Default values you want to add to the session state, if we're creating a
#         new one.
#     Example
#     -------
#     >>> session_state = get(user_name='', favorite_color='black')
#     >>> session_state.user_name
#     ''
#     >>> session_state.user_name = 'Mary'
#     >>> session_state.favorite_color
#     'black'
#     Since you set user_name above, next time your script runs this will be the
#     result:
#     >>> session_state = get(user_name='', favorite_color='black')
#     >>> session_state.user_name
#     'Mary'
#     """
#     # Hack to get the session object from Streamlit.

#     ctx = ReportThread.get_report_ctx()

#     this_session = None

#     current_server = Server.get_current()
#     if hasattr(current_server, '_session_infos'):
#         # Streamlit < 0.56
#         session_infos = Server.get_current()._session_infos.values()
#     else:
#         session_infos = Server.get_current()._session_info_by_id.values()

#     for session_info in session_infos:
#         s = session_info.session
#         if (
#             # Streamlit < 0.54.0
#             (hasattr(s, '_main_dg') and s._main_dg == ctx.main_dg)
#             or
#             # Streamlit >= 0.54.0
#             (not hasattr(s, '_main_dg') and s.enqueue == ctx.enqueue)
#             or
#             # Streamlit >= 0.65.2
#             (not hasattr(s, '_main_dg') and s._uploaded_file_mgr == ctx.uploaded_file_mgr)
#         ):
#             this_session = s

#     if this_session is None:
#         raise RuntimeError(
#             "Oh noes. Couldn't get your Streamlit Session object. "
#             'Are you doing something fancy with threads?')

#     # Got the session object! Now let's attach some state into it.

#     if not hasattr(this_session, '_custom_session_state'):
#         this_session._custom_session_state = SessionState(**kwargs)

#     return this_session._custom_session_state
