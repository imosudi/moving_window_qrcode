# Moving Window QR Code-based Attendance System

The Moving Window QR Code attendance system is an advanced digital solution that enhances security and prevents proxy attendance through dynamically changing QR codes. Here's a comprehensive description:

## System Overview

The Moving Window QR code attendance system utilises time-sensitive, constantly changing QR codes to verify student presence in real-time. Unlike static QR codes that can be shared or screenshot, these codes contain encrypted timestamps and unique identifiers that expire within a short timeframe, typically 30-60 seconds.

## Key Features

1. **Dynamic QR Generation**: The lecturer's interface continuously generates new QR codes at set intervals (e.g., every 30 seconds), displaying them on a projector or screen.

2. **Time-Window Validation**: Each QR code contains encrypted information about:
   - Module/class identifier
   - Current timestamp
   - Session-specific secrets
   - Location data (optional)

3. **Secure Scanning Process**: 
   - Students scan the displayed QR code using the mobile app or web interface
   - The system validates the scan against the current time window
   - Attendance is recorded only if the scan occurs within the valid timeframe

4. **Anti-Fraud Mechanisms**:
   - Codes expire quickly to prevent sharing
   - Each scan is tied to a specific student account
   - Device fingerprinting can be employed for additional security
   - Geofencing options can restrict attendance to within classroom boundaries

5. **Attendance Dashboard**:
   - Real-time attendance tracking for lecturers
   - Historical attendance records
   - Automated reporting and analytics

## Technical Implementation

- **Backend**: GraphQL API handling authentication, QR validation, and database interactions
- **Frontend**: Responsive web interfaces for both students and lecturers
- **Encryption**: Payload encryption to prevent tampering and reverse-engineering
- **Database**: Structured storage for modules, students, attendance records and analytics

## Benefits

- **Eliminates Proxy Attendance**: The time-sensitive nature makes it virtually impossible for students to mark attendance without being physically present
- **Efficiency**: Streamlines the attendance process compared to manual roll calls
- **Accuracy**: Reduces human error in attendance tracking
- **Flexibility**: Works across devices without requiring specialised hardware
- **Analytics**: Provides valuable insights into attendance patterns and student engagement

This modern approach to attendance management combines security with convenience, ensuring reliable presence verification while minimising disruption to valuable class time.

# Clone repo    
 git clone https://github.com/imosudi/moving_window_qrcode.git   

 cd moving_window_qrcode/    

 Create app/.env file
 touch app/.env     
Edit app/.env   
Add :

DB_HOST="m*******.com" 

DB_USER="graphqldb"

DB_PASS="PASS****WORD"

DB_NAME="graphqldb"

## Consider editing config.py    
 config,py

## Review and edit:  
 models.py vis-a-vis graphQLquery.py    
 app/models.py  
 app/graphQLquery.py     


## Create Python3 virtual environment    
 python3.9 -m venv venv

## Start virtual environment     
 source venv/bin/activate   


## Flask-Migrate 
Run:    
 flask db init   
 flask db migrate   
 flask db upgrade   

## Run       
 python main.py     


Voila!