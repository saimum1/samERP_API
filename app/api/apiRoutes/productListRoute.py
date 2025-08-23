# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.schemas import productSchema
# from app.methods import productMethod

# productListController = APIRouter()

# # ✅ Create Product
# @productListController.post("/", response_model=productSchema.ProductOut)
# def create_product(product: productSchema.ProductCreate, db: Session = Depends(get_db)):
#     if product.status not in ["available", "not_available"]:
#         raise HTTPException(status_code=422, detail="Status must be 'available' or 'not_available'")
#     print("data for create",product)
#     return productMethod.create_product(db, product)

# # ✅ List all Products
# @productListController.get("/", response_model=list[productSchema.ProductOut])
# def list_products(db: Session = Depends(get_db)):
#     data= productMethod.get_products(db)
#     print("data---->>>>>get",data)
#     return data

# # ✅ Get Single Product
# @productListController.get("/{product_id}", response_model=productSchema.ProductOut)
# def get_product(product_id: int, db: Session = Depends(get_db)):
#     db_product = productMethod.get_product_by_id(db, product_id)

#     if not db_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return db_product

# # ✅ Update Product
# @productListController.put("/{product_id}", response_model=productSchema.ProductOut)
# def update_product(product_id: int, product: productSchema.ProductUpdate, db: Session = Depends(get_db)):
#     if product.status and product.status not in ["available", "not_available"]:
#         raise HTTPException(status_code=422, detail="Status must be 'available' or 'not_available'")
#     db_product = productMethod.update_product(db, product_id, product)
#     if not db_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return db_product

# # ✅ Delete Product
# @productListController.delete("/{product_id}")
# def delete_product(product_id: int, db: Session = Depends(get_db)):
#     deleted = productMethod.delete_product_by_id(db, product_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"message": "Product deleted successfully"}


from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from app.schemas import generativeAISchema, productSchema
from app.methods import productMethod, generativeAIMethod

productListController = APIRouter()


@productListController.post("/", response_model=productSchema.ProductOut)
async def create_product(product: productSchema.ProductCreate, db = Depends(get_db)):
    if product.status and product.status not in ["available", "not_available"]:
        raise HTTPException(status_code=422, detail="Status must be 'available' or 'not_available'")
    return await productMethod.create_product(db, product)


@productListController.get("/", response_model=list[productSchema.ProductOut])
async def list_products(db = Depends(get_db)):
    return await productMethod.get_products(db)


@productListController.get("/{product_id}", response_model=productSchema.ProductOut)
async def get_product(product_id: str, db = Depends(get_db)):
    return await productMethod.get_product_by_id(db, product_id)


@productListController.put("/{product_id}", response_model=productSchema.ProductOut)
async def update_product(product_id: str, product: productSchema.ProductUpdate, db = Depends(get_db)):
    if product.status and product.status not in ["available", "not_available"]:
        raise HTTPException(status_code=422, detail="Status must be 'available' or 'not_available'")
    return await productMethod.update_product(db, product_id, product)


@productListController.delete("/{product_id}")
async def delete_product(product_id: str, db = Depends(get_db)):
    return await productMethod.delete_product_by_id(db, product_id)





@productListController.post("/generative",)
async def generative(data:generativeAISchema.ArticleRequest):
    return await generativeAIMethod.create_generative_article(data)


@productListController.post("/leadanalysis")
async def analyze_client(request: generativeAISchema.LeadAnalysisRequest):
    print("data for lead analysis", request)
    return await generativeAIMethod.analyze_leads(request)
    