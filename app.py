import streamlit as st
from streamlit_chat import message as st_message
from transformers import pipeline
import random
import string

# context = '''
# نحن شركة متخصصة فى مجال الزكاء الاصطناعى.
# نقدم العديد من الخدمات كالحلول للشركات و تدريبات فى مجال الزكاء الاصطناعى.
# التدريبات المتاحة الان هى ETE و computer vision.
# سعر ال ETE 4500 جنيه مصرى بدلا من 5000 جنيه.
# وسعر ال computer vision 6000 جنيه مصرى بدلا من 6500 جنيه مصرى.
# '''

# @st.experimental_singleton
@st.cache(allow_output_mutation=True)
def load_model():
    model = pipeline('question-answering',model='ZeyadAhmed/AraElectra-Arabic-SQuADv2-QA')
    return model
qa = load_model()


if 'count' not in st.session_state:
	st.session_state.count = 0


if st.button("Add New Context"):
	st.session_state.count += 1
	head = st.text_area("please enter your article")
	if st.session_state.count>1:
		for i in range(st.session_state.count-1):
			context = st.text_area("please enter your article", 
            key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
            




if "history" not in st.session_state:
    st.session_state.history = []



def clear():
    st.session_state["input_text"] = ""
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
            
            
            #clear()
            
    except:
        print("Empty")



st.text_input("Talk to the bot", key="input_text",on_change = generate_answer)

count = 0
for chat in st.session_state.history:
    chat['key']=count
    count +=1
    st_message(**chat)  # unpacking
    

