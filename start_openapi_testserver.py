from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Species(str, Enum):
    snake = "snake"
    unicorn = "unicorn"


class PetDetails(BaseModel):
    id: str
    name: str
    price: Optional[float]
    is_magical: bool
    species: Species


class Pet(BaseModel):
    name: str
    species: Species
    price: Optional[float]


PETS: Dict[str, PetDetails] = {}


@app.get("/", status_code=200)
def get_root() -> Dict[str, str]:
    return {"message": "Welcome to the pet store!"}


@app.post("/pets", status_code=201)
def post_pet(pet: Pet) -> PetDetails:
    if pet.species == Species.snake:
        new_pet = PetDetails(
            id=uuid4().hex,
            is_magical=False,
            **pet.dict(),
        )
    if pet.species == Species.unicorn:
        new_pet = PetDetails(
            id=uuid4().hex,
            is_magical=True,
            **pet.dict(),
        )
    PETS[new_pet.id] = new_pet
    return new_pet


@app.put("/pets/{pet_id}", status_code=200)
def put_pet(pet_id: str, pet: Pet) -> PetDetails:
    if pet_id not in PETS:
        raise HTTPException(status_code=404, detail="Pet not found")
    updated_pet = PetDetails(
        id=pet_id,
        is_magical=PETS.get(pet_id).is_magical,
        **pet.dict(),
    )
    PETS[pet_id] = updated_pet
    return updated_pet


@app.get("/pets/{pet_id}", status_code=200)
def get_pet(pet_id: str) -> PetDetails:
    if pet_id not in PETS:
        raise HTTPException(status_code=404, detail="Pet not found")
    return PETS.get(pet_id)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
