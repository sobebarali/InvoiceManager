# Invoice API

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sobebarali/InvoiceManager.git
   cd InvoiceManager
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the API**:
   - Use a browser or API client like Postman to interact with the API at `http://127.0.0.1:8000/api/invoices/`.

## Assumptions

- The `line_total` is calculated externally and provided in the payload.
- The `invoice_number` is unique for each invoice.

## Testing

- Run tests using:
  ```bash
  python manage.py test invoices
  ```

## Continuous Integration

This project uses CircleCI for continuous integration. The configuration is located in .circleci/config.yml.

- Python Version: 3.9
- Database: PostgreSQL 13.3
- Key Steps:
  - Dependency installation
  - Database migrations
  - Running tests with pytest
  - Caching for faster builds

