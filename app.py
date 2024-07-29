import logging

import streamlit as st
from google.generativeai import ChatSession, GenerativeModel, configure
from PIL import Image


def configure_client():
    """
    configure the llm settings
    """
    logging.info('Setting client configuration')

    # set client configuration
    configure(api_key=st.secrets['GEMINI_API_KEY'])
    # specify generative ai model
    client = GenerativeModel('gemini-1.5-pro')

    # set client and model in session state
    if 'client' not in st.session_state:
        st.session_state['client'] = client

    logging.info('Client configuration loaded')


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
        _prompt = prompt if prompt is str else prompt[1]
        st.markdown(_prompt)

    # add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': _prompt})

    # display assistant response in chat message container
    with st.chat_message('assistant'):
        # [BUGFIX]: directly getting response will return full object; get_chat_response() is to fix it
        stream = get_chat_response(session, prompt)
        st.write(stream)

    # add assistant response to chat history
    st.session_state.messages.append({'role': 'assistant', 'content': stream})


def main():
    st.title('Story Writer')
    st.subheader('Turn your beautiful images into well crafted stories!')

    # initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    with st.chat_message('assistant'):
        # bot initial message
        st.markdown(
            """
            Hi there 👋
            
            My self Story Writer. I am a bot 🤖 who can convert your beautiful images (illustrations, drawings, 
            paintings) into well crafted stories.
            
            I can incorporate the images that you provides into the story, or generate the story based on images ✨
            
            If you don't have images, don't worry.  
            I can also can write stories for you based on your prompts.
            
            Provide the images using the file uploader below or just prompt an idea in the text area below!
            
            > 💡Tip:  
            > Remove the previous images to enable the toggle
            """
        )

        # file uploader
        images = st.file_uploader(
            label='Upload your image(s) here!', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True
        )

        # convert images into PILLOW Image objects
        images = [Image.open(image) for image in images]

        # display images to the user if it toggled
        if st.toggle('Show Images', help='Configure before uploading an image', disabled=images != []):
            st.image(images, use_column_width=True)

    # display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    logging.info('Starting chat session...')
    session = st.session_state['client'].start_chat()
    logging.info('Chat session started!')

    # write a prompt for generating story based on images if present
    if images:
        # TODO: add functionality to process multiple images at once
        chat(session, [images[0], 'Write a beautiful story based on provided image'])

    # react to user input
    if prompt := st.chat_input('Share some thoughts about your story...'):
        chat(session, prompt)


if __name__ == '__main__':
    # set configuration
    configure_client()

    main()
