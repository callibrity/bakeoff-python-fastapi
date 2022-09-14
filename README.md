#  Setting up a development evvironment on a mac....
I prefer to use brew, so 
brew update
brew upgrade - if needed
brew search python
brew install python3

I create an alias so I can just type python and it runs python3


Create a Python Virtual Environment to isolate dependencies
python -m venv my_env
so in our case, I would suggest
python -m venv py-api
Now activate the Virtual Environment
source py-api/bin/activate

Now install the packages in the requirements.txt file
pip install -r requirements.txt

If you have trouble with psycopg2-binary, do the following:
brew install postgresql
brew install openssl
brew link openssl

export LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openssl@1.1/include"

rerun the pip install -r requirements.txt


For now, to start the app
    Start database using 'docker compose up'
    Start the Uvicorn server
    "python ./src/main.py"
    
    Look at the Swagger ( provided by fastapi) 
    http://localhost:9000/docs

    ( fastapi is built on top of OpenAPI standard, alt. will contain JSON schemas of our Pydantic models )
    Alternative 
    http://localhost:9000/redoc



# Trying to run pydantic-docs datamodel code generator on the openapi.json

model1.py is generated off of the above...  It is not currently being used in the code.