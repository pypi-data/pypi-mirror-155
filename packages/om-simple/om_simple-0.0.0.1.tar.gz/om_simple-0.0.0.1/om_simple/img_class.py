
import torch
from PIL import Image
from om_simple.img_class_model import ImageTransform, SimpleModel
from om_simple.tools.utils import chunk_list


class ImageClassification(object):
    def __init__(self, model_path, device="cuda") -> None:
        self.model = SimpleModel.load_from_checkpoint(model_path)              
        self.model.eval()
        self.model.to(device)  
        self.transform = ImageTransform(False)
        self.device = device
        self.labels =  {y: x for x, y in self.model._hparams.class_to_index.items()}
            
    def predict(self, images: list): # labels e.g., {0: "abnormal":, 1:"normal"}     
        results = []
        for _imgs in chunk_list(images):     
            with torch.no_grad():
                predicts = self.model(torch.stack([self.transform(Image.open(x).convert('RGB')).to(self.device) for x in _imgs]))
                predicts = torch.nn.functional.softmax(predicts).max(1)            
            results.extend([{"pred": self.labels[x], "score":y} for x,y in zip(predicts.indices.cpu().numpy().tolist(),predicts.values.cpu().numpy().tolist())])
        return results
        

