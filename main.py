from typing import List
from pydantic import BaseModel, ConfigDict

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# База данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./recipes.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class RecipeDB(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cooking_time = Column(Integer)
    views = Column(Integer, default=0)
    ingredients = Column(Text)
    description = Column(Text)


Base.metadata.create_all(bind=engine)


# Pydantic модели с ConfigDict
class RecipeCreate(BaseModel):
    title: str
    cooking_time: int
    ingredients: str
    description: str
    model_config = ConfigDict(from_attributes=True)


class RecipeList(BaseModel):
    id: int
    title: str
    views: int
    cooking_time: int
    model_config = ConfigDict(from_attributes=True)


class RecipeDetail(BaseModel):
    id: int
    title: str
    cooking_time: int
    ingredients: str
    description: str
    views: int
    model_config = ConfigDict(from_attributes=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="Кулинарная книга API",
    description="API для кулинарной книги с рецептами",
    version="1.0.0",
)


@app.post("/recipes/", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = RecipeDB(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return RecipeDetail.model_validate(db_recipe)


@app.get("/recipes/", response_model=List[RecipeList])
async def get_recipes(db: Session = Depends(get_db)):
    result = (
        db.query(RecipeDB)
        .order_by(RecipeDB.views.desc(), RecipeDB.cooking_time.asc())
        .all()
    )
    return [RecipeList.model_validate(r) for r in result]


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    recipe.views += 1
    db.commit()
    return RecipeDetail.model_validate(recipe)
