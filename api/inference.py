import torch
from torchvision import models, transforms
from PIL import Image

# Define the model architecture
weights = models.EfficientNet_B4_Weights.DEFAULT
model = models.efficientnet_b4(weights=weights)
num_classes = 5 
model.classifier = torch.nn.Sequential(
    torch.nn.Dropout(p=0.3, inplace=True),
    torch.nn.Linear(model.classifier[1].in_features, num_classes)
)

# Load the model state dictionary
model.load_state_dict(torch.load('api/model/best_model.pth', map_location=torch.device('cpu'), weights_only=True))
model.eval()

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Define the label mapping  
label_mapping = {0: 'Heart', 1: 'Oblong', 2: 'Oval', 3: 'Round', 4: 'Square'}

def predict_face_shape(image_path):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.inference_mode():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    
    return label_mapping[predicted.item()]