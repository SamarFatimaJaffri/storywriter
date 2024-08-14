import logging

import streamlit as st
from google.generativeai import ChatSession, GenerativeModel, configure
from PIL import Image


def add_variable(variable, value):
    """
    add session variables
    :param variable: name of the variable
    :param value: (initial) value of the variable
    """
    if variable not in st.session_state:
        st.session_state[variable] = value


def set_session_state():
    """
    set session state variables
    """
    logging.info('Setting session variables')
    # initialize chat history
    add_variable('messages', [])

    # add session variables to store images and toggle value to session
    add_variable('images', [])
    add_variable('toggle', False)
    logging.info('Session variables loaded')


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
    add_variable('client', client)
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


@st.dialog('Upload your images')
def upload_images():
    # file uploader
    images = st.file_uploader(
        label='Upload your image(s) here!', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True
    )
    # display images toggle
    toggle = st.toggle(
        'Show Images', help='Configure before uploading an image', disabled=images != []
    )

    # refresh after the pictures have been uploaded
    if st.button('Upload'):
        st.session_state.toggle = toggle
        st.session_state.images = images
        st.rerun()


def main():
    st.title('Story Writer')
    st.subheader('Turn your beautiful images into well crafted stories!')

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
            
            Provide the images by calling image dialog or just prompt an idea in the text area below!
            
            > 💡Tip:  
            > Call image dialog using `\images` command.
            """
        )

    # display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            if message.get('img', None):
                st.image(message['img'], width=300)

    logging.info('Starting chat session...')
    session = st.session_state['client'].start_chat()
    logging.info('Chat session started!')

    # react to user input
    if prompt := st.chat_input('Share some thoughts about your story...'):
        if prompt == '\\images':
            upload_images()
        else:
            chat(session, prompt)
    elif st.session_state.images:
        # convert images into PILLOW Image objects
        images = [Image.open(image) for image in st.session_state.images]
        logging.info('Images uploaded!')

        # write a prompt for generating story based on images if present
        if images:
            # TODO: add functionality to process multiple images at once
            chat(session, [images[0], 'Write a beautiful story based on provided image'])


if __name__ == '__main__':
    # set client and session configuration
    configure_client()
    set_session_state()

    main()
