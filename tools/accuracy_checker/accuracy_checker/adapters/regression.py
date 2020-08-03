"""
Copyright (c) 2018-2020 Intel Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy as np

from .adapter import Adapter
from ..representation import RegressionPrediction


class RegressionAdapter(Adapter):
    """
    Class for converting output of regression model to RegressionPrediction representation
    """

    __provider__ = 'regression'
    prediction_types = (RegressionPrediction, )

    def process(self, raw, identifiers, frame_meta):
        """
        Args:
            identifiers: list of input data identifiers
            raw: output of model
            frame_meta: list of meta information about each frame
        Returns:
            list of RegressionPrediction objects
        """
        predictions = self._extract_predictions(raw, frame_meta)[self.output_blob]
        if len(np.shape(predictions)) == 1:
            predictions = np.expand_dims(predictions, axis=0)
        predictions = np.reshape(predictions, (predictions.shape[0], -1))

        result = []
        for identifier, output in zip(identifiers, predictions):
            prediction = RegressionPrediction(identifier, output)
            result.append(prediction)

        return result
