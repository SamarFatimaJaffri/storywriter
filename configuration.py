import logging

import streamlit as st
from google.generativeai import GenerativeModel, configure


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
