# Data Engineer Dashboard

## Features
- Main Dashboard
- Airflow
    - Dag list
    - Run / pause dag
    - Task list
- Alert Management System
    - Alert list
    - Error list
    - Enable/stop checking process
- CDC Dashboard
    - CDC list
    - CDC validity
    - Connector & task status
    - Error logs
- ETL Dashboard
    - Execution histories
    - Estimation time for realtime
- NIFI Dashboard
    - Group data list
    - Processor details
    - Turn off/on the processor (scheduler)
- Validation and Recovery
    - Validation Data List
    - Recovery Data List
    - Recovery Now
    - Recovery Scheduler & Auto Execution

## Instalation
- setup the environment file
```sh
see for details at env.sample file
```
- install the requirements
```sh
pip install -r requirements.txt
```

- migrate the migration files
```sh
python manage.py migrate
```

- create a user using django shell script
```sh
python manage.py shell

from users.models import User
>>> user=User.objects.create_user('user_de@majoo.id', 'majOO#2022')
>>> user.is_superuser=True
>>> user.is_staff=True
>>> user.is_active=True
>>> user.save()
```

- run server
```sh
python manage.py runserver
```

## [1.4.0] - 2023-08-01
- initialize changelog [muhammad.muzakki@majoo.id]
- fix/recovery-etl-product [akbar.noto@majoo.id]
### Changed
- apps/home/models.py
    ``added recovery accounting history table``
- apps/home/apis/etl_apis.py
    ``added etl monitoring for hotfix live recovery``
    
## [1.0.7] - 2022-09-29
- Bug Fixing

## [1.0.0] - 2022-09-14
- initial project
