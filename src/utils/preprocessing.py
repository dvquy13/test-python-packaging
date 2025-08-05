def preprocess_data(data):
    """Example preprocessing function"""
    return data.strip().lower()

def validate_input(input_data):
    """Example validation function"""
    if not input_data:
        raise ValueError("Input data cannot be empty")
    return True