from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import selectinload

# База данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./recipes.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Модель БД
class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # название блюда
    cooking_time = Column(Integer)  # время приготовления в минутах
    views = Column(Integer, default=0)  # количество просмотров
    ingredients = Column(Text)  # список ингредиентов (JSON или разделённый запятыми)
    description = Column(Text)  # текстовое описание


Base.metadata.create_all(bind=engine)


# Pydantic модели для валидации
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


# Dependency для сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="Кулинарная книга API",
    description="API для кулинарной книги с рецептами. Поддерживает список рецептов (сортировка по популярности), детали рецепта и создание новых.",
    version="1.0.0"
)


@app.post("/recipes/", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """
    Создать новый рецепт.

    - **title**: Название блюда (обязательно)
    - **cooking_time**: Время приготовления в минутах (целое число > 0)
    - **ingredients**: Список ингредиентов через запятую или JSON-массив строк
    - **description**: Подробное текстовое описание приготовления

    Возвращает созданный рецепт с сгенерированным ID.
    """
    db_recipe = RecipeDB(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return RecipeDetail.from_orm(db_recipe)


@app.get("/recipes/", response_model=List[RecipeList])
async def get_recipes(db: Session = Depends(get_db)):
    """
    Получить список всех рецептов.

    Сортировка:
    1. По убыванию количества просмотров (views DESC)
    2. При равенстве views — по возрастанию времени приготовления (cooking_time ASC)

    Поля для фронтенда: title, views, cooking_time.
    """
    result = db.query(RecipeDB).order_by(
        RecipeDB.views.desc(), RecipeDB.cooking_time.asc()
    ).all()
    return [RecipeList.from_orm(r) for r in result]


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    """
    Получить детальную информацию о рецепте.

    - **recipe_id**: ID рецепта (целое число > 0)

    Увеличивает счётчик просмотров (views) на 1 при каждом вызове.
    Если рецепт не найден — 404 ошибка.

    Поля: title, cooking_time, ingredients, description, views (обновлённый).
    """
    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    recipe.views += 1  # Инкремент просмотров
    db.commit()
    return RecipeDetail.from_orm(recipe)
