import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms

import numpy as np 

class LandmarkEmbedding(nn.Module):
    def __init__(self, input_dim, emb_dim = 128):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),  nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, emb_dim)
        )

    def forward(self, X):
        z = self.net(X)
        return F.normalize(z, p=2, dim=1)
        
class HandNormalizer:
    def __init__(self, wrist_idx=0):
        self.wrist_idx = wrist_idx

    def __call__(self, landmarks):
        landmarks = np.array(landmarks).reshape(-1, 3)

        # 1. Translate: wrist at origin
        wrist = landmarks[self.wrist_idx]
        landmarks -= wrist

        # 2. Scale: max distance from wrist to any point = 1
        scale = np.max(np.linalg.norm(landmarks, axis=1))
        if scale > 1e-8:
            landmarks /= scale

        return landmarks.flatten()

class HandFeature:
    def __init__(self, methods=["coords", "distances", "angle"]):
        self.methods = methods

    def __call__(self, landmarks):
        landmarks = np.array(landmarks).reshape(-1, 3)

        features = []

        if "coords" in self.methods:
            features.extend(landmarks.flatten())

        if "distances" in self.methods:
            for i in range(len(landmarks)):
                for j in range(i+1, len(landmarks)):
                    dist = np.linalg.norm(landmarks[i] - landmarks[j])
                    features.append(dist)
                    
        if "angle" in self.methods:
            finger_chains = [
                [0, 1, 2, 3, 4],     # Thumb
                [0, 5, 6, 7, 8],     # Index
                [0, 9, 10, 11, 12],  # Middle
                [0, 13, 14, 15, 16], # Ring
                [0, 17, 18, 19, 20]  # Pinky
            ]
            for chain in finger_chains:
                for k in range(len(chain)-2):
                    v1 = landmarks[chain[k+1]] - landmarks[chain[k]]
                    v2 = landmarks[chain[k+2]] - landmarks[chain[k+1]]
                    cosang = np.dot(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
                    angle = np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))
                    features.append(angle)

        return np.array(features, dtype=np.float32)


def converter(embeded, prototype, label):
    similarities = F.cosine_similarity(embeded, prototype)
    # print(similarities)  # higher = more similar
    best_idx = torch.argmax(similarities)

    return label[best_idx]