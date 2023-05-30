import os
import zipfile
import json
import pickle

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.model import MatchSchema

router = APIRouter()

zip_file_path = 'models.zip'
extract_dir = 'models/'
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
  zip_ref.extractall(extract_dir)

with open("models/model_home.pkl", "rb") as home_file:
  model_home = pickle.load(home_file)

with open("models/model_away.pkl", "rb") as away_file:
  model_away = pickle.load(away_file)

# Load the label encoder transformations and the models
with open("server/label_encoder_transformations.json", "r") as json_file:
  reverse_transformation = json.load(json_file)


def find(lst, val: int):
  for key, value in lst.items():
    if val == value:
      return key
    

@router.post("/")
def predict(match: MatchSchema = Body(...)) -> dict:
  neutral = 1
  match = jsonable_encoder(match)

  # Read the input data
  home_team = match["home_team"]
  away_team = match["away_team"]
  country = match["country"]

  # Check if the home team and away team are the same
  if home_team == country or away_team == country:
    neutral = 0

  # Transform the input data
  home_team = reverse_transformation["home_team"][home_team]
  away_team = reverse_transformation["away_team"][away_team]
  country = reverse_transformation["country"][country]

  # Check if the home team and away team are the same
  if home_team == away_team:
    return {"message": "Home team and away team must be different."}


  # Predict the home team score
  home_team_score = model_home.predict([[home_team, away_team, country, neutral]])

  # Predict the away team score
  away_team_score = model_away.predict([[away_team, home_team, country, neutral]])

  # Round the scores
  int_home_team_score = round(home_team_score[0])
  int_away_team_score = round(away_team_score[0])

  # Check if the home team won
  if int_home_team_score > int_away_team_score:
    winner = find(reverse_transformation["home_team"], home_team)
  elif int_home_team_score < int_away_team_score:
    winner = find(reverse_transformation["away_team"], away_team)
  else:
    winner = "Draw"

  # Return the result
  return {
    "home_team": find(reverse_transformation["home_team"], home_team),
    "away_team": find(reverse_transformation["away_team"], away_team),
    "country": find(reverse_transformation["country"], country),
    "neutral": find(reverse_transformation["neutral"], neutral) == "True",
    "home_team_score": round(int_home_team_score),
    "away_team_score": round(int_away_team_score),
    "winner": winner
  }
