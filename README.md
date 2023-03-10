# generative-stalagmite


This uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. 

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd generative-stalagmite
   ```

4. Create a new virtual environment:

	Linux:
   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```
   
   Windows:
   ```bash
   $ python -m venv venv
   $ .\venv\Scripts\activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   $ pip install --upgrade openai
   ```


6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

Now go to [http://localhost:5000/stalagmite](http://localhost:5000/stalagmite) ! Each load of the page will generate a new stalagmite. 

To modify the OpenAI prompt, edit the `PROMPT` variable in he .env file.