# **This is the BlockCyper Transaction Monitoring Exercise**


### Here I have used the MYSQL database that is hosted in the cloud _"aiven"_. The credentials and connection details are stored in the config files


#### Before running this exercise we have to install the requirements.txt file which contains the necessary Python libraries that are used in the exercise (Python is prerequisite).
    cmd: pip install -r requirements.txt

### To start up the API and run the job that fetches the Blockchain transactions we have to run the "main.py" inside the src/server
    cmd: python src/server/__main__.py

### URL to access the endpoint (blockchain_data)
    http://0.0.0.0:8091/docs

### We can pass this payload to the endpoint, _**"num_of_records"**_ which is by default _**"10"**_. This specifies the number of latest records that are to be retrieved for the relational database.
    {"num_of_records": 5}
}
### To run the test cases we can execute the test_api.py and test_methods.py files. 



