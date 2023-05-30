from pydantic import BaseModel

class MatchSchema(BaseModel):
  home_team: str
  away_team: str
  country: str

  class Config:
    schema_extra = {
      "example": {
        "home_team": "England",
        "away_team": "France",
        "country": "England"
      }
    }
