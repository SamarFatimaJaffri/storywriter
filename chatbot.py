import streamlit as st
from google.generativeai import ChatSession


class ChatBot:
    def __init__(self):
        # start chat session
        self.session: ChatSession = st.session_state['client'].start_chat()

    def get_chat_response(self, prompt: str | list) -> str:
        """
        get the prompt response from the llm
        :param prompt: user prompt or image to story prompt with image
        :return: llm response
        """
        responses = self.session.send_message(prompt, stream=True)

        return ''.join([chunk.text for chunk in responses])

    def chat(self, prompt: str | list):
        """
        chat with the bot
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
            stream = self.get_chat_response(prompt)
            st.write(stream)

        # add assistant response to chat history
        st.session_state.messages.append({'role': 'assistant', 'content': stream})
