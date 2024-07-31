# Story Writer
Hi there 👋
            
My self Story Writer. I am a bot 🤖 who can convert your beautiful images (illustrations, drawings, 
paintings) into well crafted stories.

I can incorporate the images that you provides into the story, or generate the story based on images ✨

If you don't have images, don't worry.  
I can also can write stories for you based on your prompts.

Just provide the images using the file uploader or just prompt an idea in the text area!

> 💡Tip:  
> Remove the previous images to re-enable the toggle

## Managing Dependencies

To add libraries into the requirements.txt file run,  
`pip freeze > requirements.txt`

For removing specific libraries along with its dependencies install pip-autoremove library.  
`pip-autoremove library-name`

## Installing Dependencies

Before installing the dependencies create a virtual environment & make sure the virtual environment is active. 
You can create a virtual environment in your IDE using options or by using command,  
`python -m venv c:\path\to\myenv`

After activating the virtual environment active it by the following command in windows,  
`.venv/Scripts/activate`

After the .venv is activated now install the dependencies by executing the following command,  
`pipenv install -r requirements.txt`

pip could have been used to install dependencies as follows,  
`pip install -r requirements.txt`.  
But as we are using pipenv, we are using it for installation.

## Setup pre-commit

Pre-commit is the library that lets you execute checks locally before pushing the changes to remote repository.
Install pre-commit using pip,  
`pip install pre-commit`

After installing pre-commit library, run `pre-commit install` to install pre-commit in git hooks. pre-commit will now
run before every commit, or on the stages specified in pre-commit config file as default_stages.
You can check the list of supported stages here -> https://pre-commit.com/#supported-git-hooks

Create a pre-commit file and name it as `.pre-commit-config.yaml`. Now inside this file you can create the hooks by
specifying the repository, revision, and hooks names.

## Running the application

### Accessing application

This application is deployed at Streamlit community cloud and if you want to access the application you can do so by
accessing this link https://story-writer.streamlit.app/

### Starting app locally

Or if you want to locally start the application you can do that by executing the command,  
`streamlit run app.py`
