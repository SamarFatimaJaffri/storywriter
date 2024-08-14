import streamlit as st
from google.generativeai import ChatSession


def get_chat_response(session: ChatSession, prompt: str | list) -> str:
    """
    get the prompt response from the llm
    :param session: chat session
    :param prompt: user prompt or image to story prompt with image
    :return: llm response
    """
    responses = session.send_message(prompt, stream=True)

    return ''.join([chunk.text for chunk in responses])


def chat(session: ChatSession, prompt: str | list):
    """
    chat with the bot
    :param session: chat session
    :param prompt: user prompt or image to story prompt with image
    :return: None
    """
    # display user message in chat message container
    with st.chat_message('user'):
        img, _prompt = (None, prompt) if isinstance(prompt, str) else prompt
        st.markdown(_prompt)

        # display images to the user if it toggled
        if img and st.session_state.toggle:
            st.image(img, width=300)

    # add user message to chat history
    st.session_state.messages.append({
        'role': 'user', 'content': _prompt, 'img': img if st.session_state.toggle else None
    })

    # display assistant response in chat message container
    with st.chat_message('assistant'):
        # [BUGFIX]: directly getting response will return full object; get_chat_response() is to fix it
        stream = get_chat_response(session, prompt)
        st.write(stream)

    # add assistant response to chat history
    st.session_state.messages.append({'role': 'assistant', 'content': stream})
