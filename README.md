<h1>Please follow the below steps to setup MyCurrency Project</h1>
1. Install python 3.11 <br/>
2. Install rabbitmq for queueing process by below command <br/>
sudo apt-get install rabbitmq-server
3. Start rabbitmq service <br/>
sudo systemctl start rabbitmq-server
4. Install python libraries <br/>
pip install django djangorestframework django-cors-headers pytest pytest-django asyncio adrf pika <br/>
Above are neccessory packages to execute the project. others packages are present in requirements.txt file that also can be install.
5. Enable rabbitmq plugins to see rabbitmq dashboard <br/>
sudo rabbitmq-plugins enable rabbitmq_management <br/>
http://localhost:15672. Default credentials are guest/guest.
6. Take clone from the git repo <br/>
Go to mycurrency folder then run the server start command <br/>
py manage.py runserver <br/>
7. Open new terminal and execute rabbitmq consumer by below command <br/>
Go to mycurrency project folder and run python exchange/consumer.py
<br/>
<br/>
I have used async with adrf package which can be seen by currency-rates-list api and concurrency have used via async queque process. 
<br/>
For Queue process I have used rabbitmq to send the message to consumer and consumer will store the data database from the external provider api. This api can be verify by exchange-rates-list api.
<br/>

Testcase also implemented for storing the data into database from provider. This can be run by command <br/>
pytest exchange/tests/test_historical_store.py
