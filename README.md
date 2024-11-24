<h1>Please follow the below steps to setup MyCurrency Project</h1>
1. Install python 3.11 <br/>
2. Install rabbitmq for queueing process by below command <br/>
sudo apt-get install rabbitmq-server
3. Start rabbitmq service <br/>
sudo systemctl start rabbitmq-server
4. Install python libraries <br/>
pip install django djangorestframework django-cors-headers pytest pytest-django asyncio adrf pika <br/>
5. Take clone from the git repo <br/>
Go to mycurrency folder then run the server start command <br/>
py manage.py runserver

  
