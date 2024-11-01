import logging

import streamlit as st
from google.generativeai import GenerativeModel, configure


class Configuration:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.session_state_set = False
        self.client_configured = False

    @staticmethod
    def _add_variable(variable, value):
        """
        add session variables
        :param variable: name of the variable
        :param value: (initial) value of the variable
        """
        if variable not in st.session_state:
            st.session_state[variable] = value

    def set_session_state(self):
        """
        set session state variables
        """
        logging.info('Setting session variables')
        # initialize chat history
        self._add_variable('messages', [])

        # add session variables to store images and toggle value to session
        self._add_variable('images', [])
        self._add_variable('toggle', False)
        logging.info('Session variables loaded')

        # set session state flag to true
        self.session_state_set = True

    def configure_client(self, gemini_api_key):
        """
        configure the llm settings
        """
        logging.info('Setting client configuration')

        # set client configuration
        configure(api_key=gemini_api_key)
        # specify generative ai model
        client = GenerativeModel('gemini-1.5-pro')

        # set client and model in session state
        self._add_variable('client', client)
        logging.info('Client configuration loaded')

        # set config flag to true
        if gemini_api_key:
            self.client_configured = True
