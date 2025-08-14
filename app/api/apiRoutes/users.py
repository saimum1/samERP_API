from fastapi import APIRouter, Depends, HTTPException, status
userController = APIRouter()

@userController.get('/users')
def getUser():
    return {'name':'John Doe','age':'14','blodd':'+o'}