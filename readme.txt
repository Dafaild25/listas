las librerias que instale son:
pip install fastapi uvicorn sqlalchemy pydantic[dotenv] python-multipart aiohttp

para la parte ui instalmos 
pip install streamlit requests


comandos para correr el  back
uvicorn app.main:app --reload

comando para correr el ui
streamlit run ui/main.py


para crear una  busqueda con  rapidFuzz
pip install rapidfuzz
