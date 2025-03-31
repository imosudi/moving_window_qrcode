# Moving Window QR Code graphql

# Clone repo    
 git clone https://github.com/imosudi/moving_window_qrcode.git   

 cd moving_window_qrcode/    


# Create app/.env file
 touch app/.env     
Edit app/.env   
Add :

DB_HOST="m*******.com" 

DB_USER="graphqldb"

DB_PASS="PASS****WORD"

DB_NAME="graphqldb"

# Consider editing config.py    
 config,py

# Review and edit:  
 models.py vis-a-vis graphQLquery.py    
 app/models.py  
 app/graphQLquery.py     


# Create Python3 virtual environment    
 python3 -m venv venv

# Start virtual environment     
 source venv/bin/activate   


# Flask-Migrate 
Run:    
 flask db init   
 flask db migrate   
 flask db upgrade   

# Run       
 python main.py     


Voila!