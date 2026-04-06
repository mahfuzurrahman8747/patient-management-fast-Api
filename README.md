# Patient Management API

> A FastAPI-based REST API for managing patient health records with BMI calculation and health status tracking.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Features

- ✅ **Create Patients**: Add new patient records with full health information
- ✅ **Read Patients**: Retrieve single patient or view all patients
- ✅ **Update Patients**: Modify existing patient health data
- ✅ **Delete Patients**: Remove patient records
- ✅ **BMI Calculation**: Automatic BMI computation from height and weight
- ✅ **Health Status**: Automatic health verdict (Underweight, Normal, Overweight, Obese)
- ✅ **Sort & Filter**: Sort patients by height, weight, or BMI
- ✅ **JSON Storage**: Persistent data storage using JSON
- ✅ **Data Validation**: Pydantic models for type safety
- ✅ **Interactive Docs**: Auto-generated Swagger UI documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/patient-management-api.git
   cd patient-management-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn pydantic
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Endpoints

### Get Home Information
```http
GET /
```
Returns a welcome message.

### Get About Information
```http
GET /about
```
Returns API description.

### View All Patients
```http
GET /views
```
Retrieves all patient records.

**Response:**
```json
{
  "P001": {
    "name": "Ananya Verma",
    "city": "Guwahati",
    "age": 28,
    "gender": "female",
    "height": 1.65,
    "weight": 90.0,
    "bmi": 33.06,
    "health_status": "Obese"
  }
}
```

### Get Single Patient
```http
GET /patient/{patient_id}
```
Retrieves a specific patient by ID.

**Example:**
```http
GET /patient/P001
```

**Response:**
```json
{
  "name": "Ananya Verma",
  "city": "Guwahati",
  "age": 28,
  "gender": "female",
  "height": 1.65,
  "weight": 90.0,
  "bmi": 33.06,
  "health_status": "Obese"
}
```

### Sort Patients
```http
GET /sort?sort_by={field}&order={order}
```

**Parameters:**
- `sort_by` (required): `height`, `weight`, or `bmi`
- `order` (optional): `asc` (default) or `desc`

**Example:**
```http
GET /sort?sort_by=bmi&order=desc
```

### Create Patient
```http
POST /patient
```

**Request Body:**
```json
{
  "id": "P007",
  "name": "John Doe",
  "city": "Delhi",
  "age": 32,
  "gender": "Male",
  "height": 1.80,
  "weight": 85.0
}
```

**Response (201 Created):**
```json
{
  "message": "Patient created successfully"
}
```

### Update Patient
```http
PUT /edit/{patient_id}
```

**Request Body (all fields optional):**
```json
{
  "name": "John Updated",
  "age": 33,
  "weight": 87.5
}
```

**Response:**
```json
{
  "message": "Patient updated successfully"
}
```

### Delete Patient
```http
DELETE /delete/{patient_id}
```

**Response:**
```json
{
  "message": "Patient deleted successfully"
}
```

## 📁 Project Structure

```
patient-management-api/
├── main.py              # FastAPI application with all endpoints
├── patient.json         # JSON database with patient records
└── README.md           # This file
```

## 🗂️ Data Format

The `patient.json` file stores patient data in the following format:

```json
{
  "P001": {
    "name": "string",
    "city": "string",
    "age": "integer (0-120)",
    "gender": "Male or Female",
    "height": "float (meters)",
    "weight": "float (kilograms)",
    "bmi": "float (auto-calculated)",
    "health_status": "string (auto-calculated)"
  }
}
```

## 🧮 Health Status Categories

| BMI Range | Status |
|-----------|--------|
| < 18.5 | Underweight |
| 18.5 - 24.9 | Normal weight |
| 25.0 - 29.9 | Overweight |
| ≥ 30.0 | Obese |

## 💻 Usage Examples

### Using Python Requests
```python
import requests

# Create patient
new_patient = {
    "id": "P008",
    "name": "Jane Smith",
    "city": "Bangalore",
    "age": 28,
    "gender": "Female",
    "height": 1.65,
    "weight": 65.0
}

response = requests.post("http://localhost:8000/patient", json=new_patient)
print(response.json())

# Get all patients
response = requests.get("http://localhost:8000/views")
patients = response.json()
print(patients)

# Sort by BMI (descending)
response = requests.get("http://localhost:8000/sort?sort_by=bmi&order=desc")
sorted_patients = response.json()
print(sorted_patients)
```

### Using cURL
```bash
# Create patient
curl -X POST "http://localhost:8000/patient" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "P009",
    "name": "Alex Johnson",
    "city": "Mumbai",
    "age": 35,
    "gender": "Male",
    "height": 1.75,
    "weight": 80.0
  }'

# Get all patients
curl "http://localhost:8000/views"

# Sort by height
curl "http://localhost:8000/sort?sort_by=height&order=asc"

# Delete patient
curl -X DELETE "http://localhost:8000/delete/P007"
```

## 🧪 Testing

Visit http://localhost:8000/docs to access the interactive Swagger UI where you can:
- Test all endpoints
- View request/response schemas
- Try different parameters
- See real examples

## 📋 Validation Rules

- **ID**: Required, unique string
- **Name**: Required string
- **City**: Required string
- **Age**: Required, must be between 1-119
- **Gender**: Male or Female
- **Height**: Required, positive float (meters)
- **Weight**: Required, positive float (kilograms)

## ⚙️ Data Persistence

Patient data is stored in `patient.json`. Changes are automatically saved to the file when you:
- Create a new patient
- Update an existing patient
- Delete a patient

## 📝 Error Handling

The API returns appropriate HTTP status codes:
- **200 OK**: Successful GET or PUT request
- **201 Created**: Patient successfully created
- **400 Bad Request**: Invalid input or patient already exists
- **404 Not Found**: Patient ID not found
- **500 Server Error**: Internal server error

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Made with ❤️ using FastAPI**
