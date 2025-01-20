import redis
import streamlit as st

# Fetch Redis connection details from secrets
redis_host = st.secrets['REDIS_HOST']
redis_port = st.secrets['REDIS_PORT']
redis_password = st.secrets['REDIS_PASSWORD']

# Establish a connection to Redis
redis_client = redis.StrictRedis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)

# Test the connection
try:
    redis_client.ping()
    print("Connected to Redis successfully!")
except redis.exceptions.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
