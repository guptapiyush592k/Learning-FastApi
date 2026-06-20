from pydoc import allmethods
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import database_model
from models import Product
from database import engine
from database import session
from sqlalchemy.orm import Session

app = FastAPI()

#the below line is responsible to create the tables in the database
database_model.Base.metadata.create_all(bind=engine)

#the below code is handling CORS error
app.add_middleware(
    CORSMiddleware,
    allow_origin=['http://localhost:3000'],
    allow_methos=['*']
)

@app.get("/") 
def greet():
    return {"message": "Welcome to fastApi Backend"}

products = [
        Product(id=1, name="Product 1", description="Description 1", price=100, quantity=10),
        Product(id=2, name="Product 2", description="Description 2", price=200, quantity=20),
        Product(id=3, name="Product 3", description="Description 3", price=300, quantity=30),
    ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


#the below function is responsible to add the products to the database at the start of the application
def init_db():
    db= session()

    count = db.query(database_model.Product).count()

    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump())) #this line is converting the product object to a dictionary and then adding it to the database
        db.commit()

init_db()

@app.get('/products')
def get_all_products(db: Session = Depends(get_db)): #this line is getting the database session from the dependency injection
    return db.query(database_model.Product).all()

@app.get('/product/{product_id}')
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_product:
        return db_product
    return {"message": "Product not found"}

@app.post('/product')
def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = database_model.Product(**product.model_dump()) #this line is converting the product object to a dictionary and then adding it to the database
    db.add(db_product)
    db.commit()
    return db_product

@app.put('/product')
def update_producr(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return {"message": "Product updated successfully"}
    return {"message": "Product not found"}

@app.delete('/product/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}