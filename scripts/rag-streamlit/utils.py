import streamlit as st

st.title("Atyantik Chatbot")
st.subheader("Chat with webpage")
st.write("This is a simple meessage")
uploaded_files = st.file_uploader("Upload data",
                                  accept_multiple_files=True, 
                                  type="pdf")
genre = st.radio(
"What's your favorite movie genre",
[":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
index=None,
)

st.slider("Top K",2, 7, 4)

button = st.button("Submit") # boolean
print(button)

st.selectbox("Select your favorite color", ["Green", "Yellow", "Red"])

st.sidebar.markdown("""# About Us
Atyantik is a dynamic IT company with a team of techno enthusiasts boasting over a decade of experience in delivering IT solutions 
to clients across diverse industries. 
At Atyantik, we believe in providing our customers a value-driven, highly professional experience and delivering much more technically advanced, time-efficient, and cost-effective solutions.
                    """,unsafe_allow_html=True)