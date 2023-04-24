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
   ```

5. Activate the environment

   Linux:
   ```bash
   $ . venv/bin/activate
   ```
   
   Windows:
   ```powershell
   > .\venv\Scripts\activate
   ```

6. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   $ pip install --upgrade openai
   ```


7. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

8. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

9. Run the app:

   ```bash
   $ flask run
   ```

Now go to [http://localhost:5000/stalagmite](http://localhost:5000/stalagmite) ! Each load of the page will generate a new stalagmite. 

In order to batch create images, go to [http://localhost:5000/stalagmiteBatch?prompt=stalagmite&num=4](http://localhost:5000/stalagmiteBatch?prompt=stalagmite&num=4). `num` is the number of images you want to create. OpenAPI support up to 10 images per request, so if you request more than 10, it will be divided into multiple requests. All the retrieved images will be stored in a folder named with current date in PNG format. 

## Parameters
You can modify several parameters of this app in the .env file.

`RESOLUTION=1024`
Sets the horizontal and vertical resolution of the output image. Allowed values are 256,512 and 1024.
