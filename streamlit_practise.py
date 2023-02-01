import streamlit as st
import pandas as pd
import cv2
from matplotlib import pyplot as plt
from PIL import Image


img = Image.open('./wordcloud_pics/picture.png')

st.image(img)