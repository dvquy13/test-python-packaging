from src.utils.preprocessing import preprocess_data, validate_input

class ModelPredictor:
    def __init__(self):
        self.model = None
    
    def predict(self, input_data):
        """Main prediction method that uses preprocessing utilities"""
        validate_input(input_data)
        processed_data = preprocess_data(input_data)
        return f"Processed: {processed_data}"