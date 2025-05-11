# Flask eCommerce Website

A simple eCommerce website built with Flask, featuring a product listing page and detailed product views.

## Features

- Product grid display on homepage
- Detailed product pages
- Responsive design using Bootstrap
- Sample product data included

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `static/images` directory and add product images:
- headphones.jpg
- smartwatch.jpg
- backpack.jpg

4. Run the application:
```bash
flask run
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── static/            # Static files
│   └── images/        # Product images
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── home.html      # Homepage template
    └── item_details.html  # Product details template
```

## Requirements

- Python 3.8 or higher
- Flask and dependencies (listed in requirements.txt) 