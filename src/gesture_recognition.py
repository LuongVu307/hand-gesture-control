import numpy as np
import torch

from src.models.models import LandmarkEmbedding, converter

class GestureDetector:
    def __init__(self):
        
        self.model = LandmarkEmbedding(288)
        self.model.load_state_dict(torch.load('src/models/model.pth'))
        self.pipeline = torch.load("src/models/pipeline.pt")

        self.prototype, self.label = torch.tensor(np.load("src/models/prototypes.npy")), np.load("src/models/labels.npy")
        

    def get_gesture(self, landmark):
        landmark = landmark[0]
        processed = torch.tensor(np.expand_dims(self.pipeline(landmark), axis=0))

        output = self.model(processed)

        return converter(output, self.prototype, self.label)

