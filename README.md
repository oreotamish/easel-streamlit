# Easel-Streamlit

Easel is a project aimed at simplifying access.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/oreotamish/easel-streamlit.git
    ```

2. Navigate to the project directory:

    ```bash
    cd easel-streamlit
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your AWS credentials:

    ```dotenv
    encryption_key='********'
    aws_access_key_id='********'
    aws_secret_access_key='********'
    ```

## Usage

To start the Streamlit app, run the following command:

```bash
streamlit run Home.py
```