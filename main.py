from fastapi import FastAPI
import database_model
from models import Product
from database import engine
from database import Session

app = FastAPI()

#the below line is responsible to create the tables in the database
database_model.Base.metadata.create_all(bind=engine)

@app.get("/") 
def greet():
    return {"message": "Welcome to fastApi Backend"}

products = [
        Product(id=1, name="Product 1", description="Description 1", price=100, quantity=10),
        Product(id=2, name="Product 2", description="Description 2", price=200, quantity=20),
        Product(id=3, name="Product 3", description="Description 3", price=300, quantity=30),
    ]


#the below function is responsible to add the products to the database at the start of the application
def init_db():
    db= Session()

    count = db.query(database_model.Product).count()

    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump())) #this line is converting the product object to a dictionary and then adding it to the database
        db.commit()

init_db()

@app.get('/products')
def get_all_products():
    return products

@app.get('/product/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"message": "Product not found"}

@app.post('/product')
def create_product(product: Product):
    products.append(product)
    return product

@app.put('/product')
def update_producr(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product updated successfully"
    return {"message": "Product not found"}

@app.delete('/product/{product_id}')
def delete_product(product_id: int):
    for i in range(len(products)):
        if products[i].id == product_id:
            products.pop(i)
            return "Product deleted successfully"
    return {"message": "Product not found"}