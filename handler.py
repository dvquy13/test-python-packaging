from src.model.predictor import ModelPredictor

class TorchServeHandler:
    def __init__(self):
        self.predictor = ModelPredictor()
    
    def initialize(self, context):
        """Initialize the handler"""
        pass
    
    def preprocess(self, data):
        """Preprocess input data"""
        return data[0].get("body", "")
    
    def inference(self, data):
        """Run inference"""
        return self.predictor.predict(data)
    
    def postprocess(self, data):
        """Postprocess output"""
        return [{"prediction": data}]