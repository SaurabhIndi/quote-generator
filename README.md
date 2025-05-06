# Inspirational Quote Generator Streamlit App

A Streamlit web application that generates inspirational quotes based on a user-specified theme using the GPT-2 model from the `transformers` library.

## Features
- Web interface to input a theme (e.g., hope, success, love) and number of quotes (1-5).
- Display generated quotes on the page.
- Save generated quotes to a text file (`quotes.txt`) on the server.
- Simple and responsive design using Streamlit's built-in styling.

## Prerequisites
- Python 3.8 or higher
- Git
- VS Code (recommended for development)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/quote-generator.git
   cd quote-generator
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open a browser and navigate to `http://localhost:8501` (or the URL shown in the terminal).
3. Enter a theme and select the number of quotes, then click "Generate Quotes".
4. View the generated quotes on the page. Quotes are saved to `quotes.txt` in the project root.

## Example
- Input: Theme = "hope", Number of Quotes = 2
- Output:
  - Quote 1: With hope in your heart, every challenge becomes an opportunity.
  - Quote 2: Hope is the light that guides us through the darkest nights.
- Saved to `quotes.txt`

## Project Structure
- `app.py`: Streamlit application with quote generation logic and UI.
- `requirements.txt`: List of Python dependencies.
- `quotes.txt`: Output file for generated quotes (created after running the app).
- `.gitignore`: Ignores virtual environment, cache files, and output files.

## Dependencies
- `streamlit`: Web framework for the app.
- `transformers`: For the GPT-2 model and tokenizer.
- `torch`: PyTorch for model inference.

## Deployment Notes
- For production, use a platform like Streamlit Community Cloud, Heroku, or AWS.
- Ensure sufficient memory for the GPT-2 model (~500 MB).
- Streamlit apps run on port 8501 by default; configure accordingly for deployment.

## Contributing
Feel free to open issues or submit pull requests to improve the project.

## License
MIT License