from typing import List, Optional, Tuple
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from pydantic import BaseModel, ValidationError
import numpy as np
from heartdisease_model.config.core import config


# retain only the first cabin if more than
# 1 are available per passenger
le = LabelEncoder()


def change_data(col):
    if col=='Yes':
        return 1
    elif col=='No':
        return 0


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if var not in config.model_config.variables_na
        and validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data



def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    input_data['Smoking'] = input_data['Smoking'].apply(change_data)
    input_data['AlcoholDrinking'] = input_data['AlcoholDrinking'].apply(change_data)
    input_data['Stroke'] = input_data['Stroke'].apply(change_data)
    input_data['DiffWalking'] = input_data['DiffWalking'].apply(change_data)
    input_data['PhysicalActivity'] = input_data['PhysicalActivity'].apply(change_data)
    input_data['Asthma'] = input_data['Asthma'].apply(change_data)
    input_data['KidneyDisease'] = input_data['KidneyDisease'].apply(change_data)
    input_data['SkinCancer'] = input_data['SkinCancer'].apply(change_data)
    #input_data['HeartDisease'] = input_data['HeartDisease'].apply(change_data)
    #input_data['Sex'] = input_data['Sex'].apply(change_data)

    # cast numerical variables as floats
    input_data['AgeCategory'] = le.fit_transform(input_data['AgeCategory'])
    input_data['Race'] = le.fit_transform(input_data['Race'])
    input_data['GenHealth'] = le.fit_transform(input_data['GenHealth'])
    input_data['Diabetic'] = le.fit_transform(input_data['Diabetic'])

    input_data.drop(labels=config.model_config.variables_to_drop, axis=1, inplace=True)

    assert input_data.columns.tolist() == config.model_config.features
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)

    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleHeartDiseaseInputs(inputs=validated_data.replace({np.nan: None}).to_dict(orient="records"))
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors



class HeartDiseaseInputSchema(BaseModel):
    Smoking: Optional[str]
    AlcoholDrinking: Optional[str]
    Stroke: Optional[str]
    DiffWalking: Optional[str]
    AgeCategory: Optional[str]
    Race: Optional[str]
    Diabetic: Optional[str]
    PhysicalActivity: Optional[str]
    GenHealth: Optional[str]
    Asthma: Optional[str]
    KidneyDisease: Optional[str]
    SkinCancer: Optional[str]
    BMI: Optional[str]
    PhysicalHealth: Optional[str]
    MentalHealth: Optional[str]
    SleepTime: Optional[str]
    Sex: Optional[str]
     
 

  
 
  
  
  
class MultipleHeartDiseaseInputs(BaseModel):
    inputs: List[HeartDiseaseInputSchema]


