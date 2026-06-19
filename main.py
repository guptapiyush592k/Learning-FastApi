from fastapi import FastAPI
from models import Product
app = FastAPI()

@app.get("/") 
def greet():
    return {"message": "Welcome to fastApi Backend"}

products = [
        Product(id=1, name="Product 1", description="Description 1", price=100, quantity=10),
        Product(id=2, name="Product 2", description="Description 2", price=200, quantity=20),
        Product(id=3, name="Product 3", description="Description 3", price=300, quantity=30),
    ]


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