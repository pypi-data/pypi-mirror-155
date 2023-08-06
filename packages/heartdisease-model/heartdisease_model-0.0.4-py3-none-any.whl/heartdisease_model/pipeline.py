
# for encoding categorical variables
from feature_engine.encoding import OneHotEncoder, OrdinalEncoder
#from pydantic.main import Model

# for imputation

from sklearn.ensemble import RandomForestClassifier

# pipeline
from sklearn.pipeline import Pipeline

# feature scaling
from sklearn.preprocessing import LabelEncoder

from heartdisease_model.config.core import config


# set up the pipeline
heartdisease_pipe = Pipeline(
    [
        
        # encode categorical variables using one hot encoding into k-1 variables
      # ("categorical_encoder", OneHotEncoder(drop_last=True, variables=config.model_config.categorical_vars)),

      # ("label_encoder", OrdinalEncoder(variables = config.model_config.numerical_vars)),
        # scale
        (
            "Logit",
            RandomForestClassifier(
                criterion='gini',n_estimators=56,max_depth=10,max_features='log2',min_samples_split=5,min_samples_leaf=1
            ),
        ),
    ]
)
