from collections import OrderedDict

import pandas as pd
import pytest

from arthurai import ArthurAttribute, ArthurModel
from arthurai.common.constants import ValueType, Stage, InputType, OutputType
from arthurai.core.attributes import AttributeCategory

from tests.fixtures.models.regression import INT_INPUT_ATTR, FLOAT_NONINPUT_ATTR, INT_INPUT, FLOAT_NONINPUT, \
    TABULAR_MODEL_ID
from tests.fixtures.mocks import client

DOG_GROUND_TRUTH = "dog_gt"
DOG_PRED = "dog_pred"
CAT_GROUND_TRUTH = "cat_gt"
CAT_PRED = "cat_pred"

DOG_GROUND_TRUTH_ATTR = ArthurAttribute(name=DOG_GROUND_TRUTH, value_type=ValueType.Integer, stage=Stage.GroundTruth,
                                        position=0, attribute_link=DOG_PRED, categorical=True,
                                        categories=[AttributeCategory(value="0"), AttributeCategory(value="1")])
DOG_PRED_ATTR = ArthurAttribute(name=DOG_PRED, value_type=ValueType.Float, stage=Stage.PredictedValue, position=0,
                                attribute_link=DOG_GROUND_TRUTH, is_positive_predicted_attribute=True, min_range=0.,
                                max_range=1.)
CAT_GROUND_TRUTH_ATTR = ArthurAttribute(name=CAT_GROUND_TRUTH, value_type=ValueType.Integer, stage=Stage.GroundTruth,
                                        position=1, attribute_link=CAT_PRED, categorical=True,
                                        categories=[AttributeCategory(value="0"), AttributeCategory(value="1")])
CAT_PRED_ATTR = ArthurAttribute(name=CAT_PRED, value_type=ValueType.Float, stage=Stage.PredictedValue, position=1,
                                attribute_link=CAT_GROUND_TRUTH, min_range=0., max_range=1.)
PRED_TO_GT_MAP = OrderedDict()
PRED_TO_GT_MAP[DOG_PRED] = DOG_GROUND_TRUTH
PRED_TO_GT_MAP[CAT_PRED] = CAT_GROUND_TRUTH

MODEL_ATTRIBUTES = [INT_INPUT_ATTR, FLOAT_NONINPUT_ATTR, DOG_PRED_ATTR, CAT_PRED_ATTR, DOG_GROUND_TRUTH_ATTR,
                    CAT_GROUND_TRUTH_ATTR]

SAMPLE_DATAFRAME = pd.DataFrame({
    INT_INPUT: [1, 2, 1, 2, 1, 2],
    FLOAT_NONINPUT: [1., 0.5, 1., .25, .6, .9],
    DOG_PRED: [0.6, 0.8, 0.2, 0.45, 0.94, 0.12],
    CAT_PRED: [0.4, 0.2, 0.8, 0.65, 0.06, 0.88],
    DOG_GROUND_TRUTH: [0, 1, 0, 1, 1, 0],
    CAT_GROUND_TRUTH: [1, 0, 1, 0, 0, 1]
})

UNINITIALIZED_MODEL_DATA = {
        "partner_model_id": "",
        "input_type": InputType.Tabular,
        "output_type": OutputType.Multiclass,
        "display_name": "",
        "description": ""
}

MODEL_DATA_WITH_ATTRIBUTES = {
    **UNINITIALIZED_MODEL_DATA,
    "attributes": MODEL_ATTRIBUTES
}


@pytest.fixture
def initial_biclass_model(client):
    model = ArthurModel(client=client.client, **UNINITIALIZED_MODEL_DATA)
    return model

