from .core import EyEar  



#___________________#
print("import library")
run_example_usage = 0 # Change this to 0/1 to disable/enable the example usage


# Basic Imports
import os
import time
import numpy as np
from datetime import datetime
import pytz
#import requests
import io
import re
import string
import nltk
import math



# Image Processing
from PIL import Image, ImageFilter
import cv2

# Transformers for Image Processing and Translation
import torch
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    AutoTokenizer,
    AutoModelForCausalLM,
    BlipForQuestionAnswering,
    DetrImageProcessor,
    DetrForObjectDetection
)

# Text-to-Speech and Sound
from playsound import playsound
from gtts import gTTS
from pydub import AudioSegment

# Translation and OCR
from googletrans import Translator
import pytesseract

# Real-ESRGAN for Image Enhancement (if necessary, ensure it’s installed)
# from realesrgan import RealESRGANer  # Uncomment if needed

# NLP Libraries
from textblob import TextBlob
from word2number import w2n

# Voice Recognition
import speech_recognition as sr

# Firebase Setup for Intent Detection
import pyrebase
import firebase_admin
from firebase_admin import credentials, db

# Additional Libraries for Object Detection and NLP
from ultralytics import YOLO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Web Scraping
from bs4 import BeautifulSoup
from transformers import pipeline
import gc

#hand traker
import mediapipe as mp
import matplotlib.pyplot as plt








#randm
import pyrebase
import firebase_admin
from firebase_admin import credentials, db
import mediapipe as mp
import matplotlib.pyplot as plt

import torch
from PIL import Image
import numpy as np
import cv2
from transformers import DetrImageProcessor, DetrForObjectDetection, BlipProcessor, BlipForQuestionAnswering
import subprocess
import sys
import time  # Optional: for adding a delay
import re

print("finish library")
