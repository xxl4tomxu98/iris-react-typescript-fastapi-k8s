from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .iris_classifier_object import Iris_Classifier
from pydantic import BaseModel

router = APIRouter()

#creating the classifier
classifier = Iris_Classifier("iris/iris_classifier.pkl")


@router.post("/", tags=["root"])
def get_prediction(features:dict) -> dict:
    species_pred = classifier.make_prediction(features)
    response = JSONResponse({"statusCode": 200,
				             "status": "Prediction made",				
                             "result": species_pred})
    return response