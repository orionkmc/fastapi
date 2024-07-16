from pydantic import BaseModel, Field


class MovieSchema(BaseModel):
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=200)
    year: int = Field(Le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "category": "Phantasy",
                "overview": "The twilight is almost better than sunday",
                "rating": 9.5,
                "title": "Crepusculo",
                "year": "2022"
            }]
        }
    }
