import logging

import streamlit as st
from PIL import Image

from chatbot import chat
from configuration import configure_client, set_session_state


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


def startup():
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


def main():
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

    startup()
    main()
