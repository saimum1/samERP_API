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
from app.schemas.productSchema import ProductOut,ProductResponse
from typing import List
from pydantic import ValidationError



async def create_product(db, product: ProductCreate):
    doc = product.model_dump()
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()

    result = await db.products.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return ProductOut(**doc)


# async def get_products(db):
#     cursor = db.products.find().sort("updated_at", -1)
#     products = []
#     async for doc in cursor:
#         doc["_id"] = str(doc["_id"])
#         products.append(ProductOut(**doc))
#     return products



async def get_products(db):
    pipeline = [
        # Convert category_id string → ObjectId only if it exists
        {
            "$addFields": {
                "categoryObjId": {
                    "$cond": [
                        {"$and": [
                            {"$ne": ["$category_id", None]},
                            {"$regexMatch": {"input": "$category_id", "regex": "^[0-9a-fA-F]{24}$"}}
                        ]},
                        {"$toObjectId": "$category_id"},
                        None
                    ]
                }
            }
        },
        {
            "$lookup": {
                "from": "operators",
                "localField": "categoryObjId",
                "foreignField": "_id",
                "as": "operator"
            }
        },
        {
            "$unwind": {"path": "$operator", "preserveNullAndEmptyArrays": True}
        },
        {"$sort": {"updated_at": -1}}
    ]

    cursor = db.products.aggregate(pipeline)
    products = []

    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        if doc.get("operator"):
            doc["operator"]["id"] = str(doc["operator"].pop("_id"))
        products.append(ProductOut(**doc))

    print("Total products:", len(products))
    return products




async def get_products_client(db, page: int = 1, perPage: int = 8) -> ProductResponse:
    pipeline = [
        {
            "$addFields": {
                "categoryObjId": {
                    "$cond": [
                        {
                            "$and": [
                                {"$ne": ["$category_id", None]},
                                {
                                    "$regexMatch": {
                                        "input": "$category_id",
                                        "regex": "^[0-9a-fA-F]{24}$"
                                    }
                                }
                            ]
                        },
                        {"$toObjectId": "$category_id"},
                        None
                    ]
                }
            }
        },
        {
            "$lookup": {
                "from": "operators",
                "localField": "categoryObjId",
                "foreignField": "_id",
                "as": "operator"
            }
        },
        {
            "$unwind": {
                "path": "$operator",
                "preserveNullAndEmptyArrays": True
            }
        },
        {"$sort": {"updated_at": -1}},
        {"$skip": (page - 1) * perPage},
        {"$limit": perPage}
    ]

    # Count total products for pagination
    total_count = await db.products.count_documents({})
    total_pages = (total_count + perPage - 1) // perPage  # Ceiling division

    cursor = db.products.aggregate(pipeline)
    products: List[ProductOut] = []

    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        if doc.get("operator"):
            doc["operator"]["id"] = str(doc["operator"].pop("_id"))
        products.append(ProductOut(**doc))

    print("Total products:", len(products))
    return ProductResponse(
        products=products,
        totalPages=total_pages,
        totalCount=total_count
    )


async def get_product_by_id(db, product_id: str) -> ProductResponse:
    # Validate product_id
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail=f"Invalid product ID: {product_id}")
    
    try:
        obj_id = ObjectId(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing product ID: {str(e)}")

    # Aggregation pipeline
    pipeline = [
        {"$match": {"_id": obj_id}},
        {
            "$addFields": {
                "categoryObjId": {
                    "$cond": [
                        {
                            "$and": [
                                {"$ne": ["$category_id", None]},
                                {
                                    "$regexMatch": {
                                        "input": "$category_id",
                                        "regex": "^[0-9a-fA-F]{24}$"
                                    }
                                }
                            ]
                        },
                        {"$toObjectId": "$category_id"},
                        None
                    ]
                }
            }
        },
        {
            "$lookup": {
                "from": "operators",  # Verify collection name
                "localField": "categoryObjId",
                "foreignField": "_id",
                "as": "operator"
            }
        },
        {"$unwind": {"path": "$operator", "preserveNullAndEmptyArrays": True}}
    ]

    # Execute aggregation
    try:
        cursor = db.products.aggregate(pipeline)
        doc = await cursor.to_list(length=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Handle case where no document is found
    if not doc:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    # Process document
    doc = doc[0]
    doc["id"] = str(doc["_id"]) if "_id" in doc else None
    doc.pop("_id", None)
    if doc.get("operator") and isinstance(doc["operator"], dict):
        doc["operator"]["id"] = str(doc["operator"]["_id"]) if "_id" in doc["operator"] else None
        doc["operator"].pop("_id", None)
    doc["categoryId"] = str(doc["category_id"]) if doc.get("category_id") else None
    doc.pop("category_id", None)

    # Create ProductOut instance
    try:
        product = ProductOut(**doc)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Invalid product data: {str(e)}")

    return ProductResponse(
        products=[product],
        totalPages=1,
        totalCount=1
    )

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
