import logging

import streamlit as st
from PIL import Image

from chatbot import ChatBot
from configuration import Configuration


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


class StoryWriter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.config = Configuration()

    def startup(self):
        st.title('Story Writer')
        st.subheader('Turn your beautiful images into well crafted stories!')

        # set client provider
        with st.popover('Set API Key', help='Specify your Gemini API Key'):
            gemini_api_key = st.text_input(
                'Gemini API Key', placeholder='YOUR-GEMINI-API-KEY-HERE', type='password'
            )

            st.page_link(
                label='Get Gemini Key', page='https://aistudio.google.com/app/apikey',
                help='Get Gemini API Key from the official site'
            )

            # set client and session configuration
            self.config.configure_client(gemini_api_key)
            self.config.set_session_state()

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

    def main(self):
        # display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
                if message.get('img', None):
                    st.image(message['img'], width=300)

        self.logger.info('Starting chat session...')
        chatbot = ChatBot()
        self.logger.info('Chat session started!')

        # react to user input
        if prompt := st.chat_input('Share some thoughts about your story...'):
            # ask for API key if not set
            if not self.config.client_configured:
                st.info("Please add your Gemini API key to continue.")
                st.stop()

            if prompt == '\\images':
                upload_images()
            else:
                chatbot.chat(prompt)
        elif st.session_state.images:
            # convert images into PILLOW Image objects
            images = [Image.open(image) for image in st.session_state.images]
            self.logger.info('Images uploaded!')

            # write a prompt for generating story based on images if present
            if images:
                # TODO: add functionality to process multiple images at once
                chatbot.chat([images[0], 'Write a beautiful story based on provided image'])


if __name__ == '__main__':
    app = StoryWriter()

    app.startup()
    app.main()
