# Text Similarity
Text Similarity project involving manual Levenshtein Distance calculations, all packaged into a Docker container to be used as a microservice.

## Explanation of Directories

- ```Dockerfile```: Contains the information needed to build a Docker image.
- ```requirements.txt```: Lists packages that are included in the Dockerfile/Docker image.
- ```setup.sh```: Simple shell script that will build and run the Docker container microservice on port 80 of your local machine.
- ```compare_samples.sh```: Simple shell script that will run the files in ```/run```, which ping the microservice to get Levenshtein Distance between two strings.
- ```/run```
  - ```text.json```: JSON file that stores the text to be sent to the microservice. There is one "src_text" and a list of "target_text" strings.
  - ```requirements.txt```: Lists packages that are needed to ping the microservice. They are explained in the next section (step 4).
  - ```config.yml```: Config file that includes some parameters (can be changed if desired).
  - ```main.py```: Python script that calls in the text and sends requests to the model. Utilizes the ```multiprocessing``` package.
  - ```utils.py```: Utility functions to support ```main.py```.
- ```/app```
  - ```server.py```: Flask service that provides two endpoints: "/health" [GET], and "/similarity" [POST]. Accepts two strings ("src_text" and "target_text") and calculates both raw and normalized Levenshtein Distance between them.
  - ```gunicorn.sh```: Runs the Flask application through Gunicorn, a python WSGI server. Binds to port 80 and initializes 3 workers.

## Instructions to Run the Application

1. Clone this repo (```git clone https://github.com/ryanlattanzi/text_similarity save/path/local```).
2. Ensure Docker is up and ready to go.
3. cd into the repo and run ```sh setup.sh {IMAGE_TAG}```. This should build and run the docker container on ```http://0.0.0.0:80```. If you do not include an ```{IMAGE_TAG}```, it will default to 'text_sim'.
4. In ```/run```, there is a ```requirements.txt``` file that includes the ```pyyaml``` and ```requests``` library dependencies that are needed in ```main.py```. These are left for you to install in the case that you want to use virtualenv instead of installing globally.
5. Ensure that line 7 in ```compare_samples.sh``` has the correct entry (either 'python' or 'python3') for your system.
6. Finally, run ```sh compare_samples.sh``` to get an output on your terminal.
