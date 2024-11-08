import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url= "https://integrate.api.nvidia.com/v1",
    api_key="API_KEY"
)

# Function to handle question and response
def ask_question(question):
    response = ""
    
    # Call the OpenAI API in stream mode
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": question}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )

    # Stream the response as it arrives
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response+= chunk.choices[0].delta.content

    return response

# Initialize session state for history and like/dislike counts if they don't already exist
if "history" not in st.session_state:
    st.session_state.history = []
if "like_dislike_counts" not in st.session_state:
    st.session_state.like_dislike_counts = []

# Streamlit interface
st.title("Problem with your sleep?")
st.title("Speak out here.. We'r here to help! \n\n")


for i, entry in enumerate(st.session_state.history, 1):
    st.write(f"**Question {i}:** {entry['question']}")
    st.write(f"**Answer {i}:** {entry['response']}")
    
    # Display Like and Dislike buttons with counters
    cols = st.columns([1, 5, 1, 1])
    if "like" not in st.session_state.like_dislike_counts[i - 1]:
        st.session_state.like_dislike_counts[i - 1]["like"] = 0
    if "dislike" not in st.session_state.like_dislike_counts[i - 1]:
        st.session_state.like_dislike_counts[i - 1]["dislike"] = 0

    if cols[0].button("👍", key=f"like_{i}"):
        st.session_state.like_dislike_counts[i - 1]["like"] += 1
    if cols[2].button("👎", key=f"dislike_{i}"):
        st.session_state.like_dislike_counts[i - 1]["dislike"] += 1
    
    # Display like/dislike counts
    cols[1].markdown(f"Likes: {st.session_state.like_dislike_counts[i - 1]['like']} | Dislikes: {st.session_state.like_dislike_counts[i - 1]['dislike']}")
    st.write("---")  # Separator between Q&A pairs

st.subheader("Ask a New Question")

# Input for the user's question
question = st.text_area("Enter your query here:", "", key="new_question")
submit_button = st.button("Submit", key="submit_button")

# Handling the submit button
if submit_button and question:
    # Fetch response to the question
    response = ask_question(question)
    
    # Append the question and response to history
    st.session_state.history.append({"question": question, "response": response})
    st.session_state.like_dislike_counts.append({"like": 0, "dislike": 0})  # Initialize like/dislike counts

    # st.session_state.new_question = ""
    question=""
    st.experimental_rerun()  # Refresh the interface to show the new Q&A at the bottom

# Clear History button
st.sidebar.subheader("Options")
if st.sidebar.button("Clear History and Start Over"):
    st.session_state.history.clear()
    st.session_state.like_dislike_counts.clear()
    st.experimental_rerun()