import streamlit as st
import pandas as pd
import time
import json
import os
from datetime import datetime

st.set_page_config(page_title="Pro Fitness AI", layout="wide")

# 1. Database with GIF
fitness_db = {
    "Weights": [
        {"name": "Bench Press", "ar": "Chest Press", "gif": "https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif", "muscle": "Chest", "rest": 60},
        {"name": "Squat", "ar": "Squat", "gif": "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif", "muscle": "Legs", "rest": 90},
        {"name": "Deadlift", "ar": "Deadlift", "gif": "https://media.giphy.com/media/3oGRFrq6v6RwG5Z8wI/giphy.gif", "muscle": "Back", "rest": 120},
    ],
    "Cardio": [
        {"name": "Jumping Jacks", "ar": "Jumping Jacks", "gif": "https://media.giphy.com/media/3o7abKhuvqV5nF4kKY/giphy.gif", "muscle": "Full Body", "rest": 
