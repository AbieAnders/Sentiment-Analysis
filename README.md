Steps to run the application:

1) Clone the project from the remote repository to a local repository:

git clone https://github.com/AbieAnders/Sentiment-Analysis.git
cd Sentiment-Analysis

2) Create and activate a python virtual environment:

python -m venv venv
venv\Scripts\activate

3) Install all the dependencies using the command:

pip install -r requirements.txt

4) Open 2 terminal sessions, 1 for the frontend and 1 for the backend.

4) Running FastAPI

cd server
uvicorn main:app --reload

5) Running Streamlit

cd client
streamlit run main.py

Models used:

1) The first model used(KeyBERT) is a freely available model and is used for generating keywords out of the users input string.

2) I also explored using gemini but it was too slow for me.

3) I used this huggingface model 'sshleifer/distilbart-cnn-12-6' for article summarization.