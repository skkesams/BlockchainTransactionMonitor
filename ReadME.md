# **This is the BlockCyper Transaction Monitoring Exercise**


### Here I have used the MYSQL database that is hosted on the Aiven cloud. The credentials and connection details to access the data are stored inside config files


#### To run this program we have to install the requirements.txt file which contains the necessary Python libraries (Having Python installed is a prerequisite).
    cmd: pip install -r requirements.txt

### To start the API service and run the job that fetches the Blockchain transactions, we need to run the "__main__.py" file using the following command
    cmd: python src/server/__main__.py

### URL to access the API endpoint (/blockchain_data)
    http://0.0.0.0:8091/docs

### We can pass the following payload to the endpoint. This specifies the number of latest records that are to be retrieved for the relational database(default value is 10).
    {"num_of_records": 5} 
    
### To run the test cases we can execute the test_api.py and test_methods.py files. 
