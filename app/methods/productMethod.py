# from sqlalchemy.orm import Session,joinedload
# from app.models.productlist import Product
# from app.models.operators import Operator
# from app.schemas import productSchema
# from sqlalchemy.sql import cast
# from sqlalchemy import Integer,desc


# def create_product(db: Session, product: productSchema.ProductCreate):

#     print("data-------->>>>>",product)
#     db_product = Product(**product.dict())
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product


# def get_products(db: Session):
#     products = db.query(Product).options(joinedload(Product.operator)).order_by(desc(Product.updated_at)).all()
#     return products
 

# def get_product_by_id(db: Session, product_id: int):
#     return db.query(Product).filter(Product.id == product_id).first()


# def update_product(db: Session, product_id: int, product: productSchema.ProductUpdate):
#     db_product = get_product_by_id(db, product_id)
#     if not db_product:
#         return None
#     for key, value in product.dict(exclude_unset=True).items():
#         setattr(db_product, key, value)
#     db.commit()
#     db.refresh(db_product)
#     return db_product


# def delete_product_by_id(db: Session, product_id: int):
#     print("product_id",product_id)  
#     db_product = get_product_by_id(db, product_id)
#     if not db_product:
#         return None
#     db.delete(db_product)
#     db.commit()
#     return True



from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from app.models.productlist import ProductCreate, ProductUpdate, ProductOut

async def create_product(db, product: ProductCreate):
    doc = product.model_dump()
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()

    result = await db.products.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return ProductOut(**doc)


async def get_products(db):
    cursor = db.products.find().sort("updated_at", -1)
    products = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        products.append(ProductOut(**doc))
    return products


async def get_product_by_id(db, product_id: str):
    doc = await db.products.find_one({"_id": ObjectId(product_id)})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    doc["_id"] = str(doc["_id"])
    return ProductOut(**doc)


async def update_product(db, product_id: str, product: ProductUpdate):
    update_data = {k: v for k, v in product.model_dump(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update")
    update_data["updated_at"] = datetime.utcnow()

    result = await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    updated = await db.products.find_one({"_id": ObjectId(product_id)})
    updated["_id"] = str(updated["_id"])
    return ProductOut(**updated)


async def delete_product_by_id(db, product_id: str):
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully", "id": product_id}
