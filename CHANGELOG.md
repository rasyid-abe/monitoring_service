## [1.13.1] - 2023-10-09
- fix/disable-force-start-nifi [muhammad.muzakki@majoo.id]
### Changes
- apps/home/scheduler.py 
`` disable force start nifi processor``


## [1.13.0] - 2023-10-03
- feature/etl-caller [muhammad.muzakki@majoo.id]
### Adds
- apps/home/jobs/etl_caller.py 
- apps/home/apis/etl_caller_apis.py 
- apps/static/assests/etl_caller.js 
- apps/templates/home/etl_caller.html 
`` add etl caller as NIFI alternative ``

### Changes
- apps/home/scheduler.py 
- apps/home/urls.py
- apps/home/Models/etl_history.py
- apps/home/view.py
- apps/home/jobs/etl_caller.py
- apps/templates/includes/sidebar.html
`` add etl caller & its CRUD page``

## [1.12.0] - 2023-10-03
- feature/data-movement [muhammad.muzakki@majoo.id]
### Changes
- apps/home/apis/etl_apis.py 
- apps/templates/home/etl.html
`` update data movement column ``

## [1.11.0] - 2023-09-14
- feature/akunting-v2 [akbar.noto@majoo.id]
### Changes
- apps/home/apis/etl_apis.py 
- apps/home/Models/etl_history.py  `` Add model for akunting v2 ``

## [1.10.0] - 2023-09-11
- feature/etl-dashboard [abdur.rasyid@majoo.id]
### Changes
- apps/home/apis/etl_apis.py
- apps/home/jobs/nifi.py
- apps/home/Models/etl_history.py
    ``add sales dashboard ETL``

## [1.9.0] - 2023-09-04
- feature/dynamic-threshold-alert [muhammad.muzakki@majoo.id]
### Changes
- apps/home/views.py
- apps/home/apis/alert_apis.py
- apps/home/apis/etl_apis.py
- apps/home/Models/apps.py
- apps/home/templates/alert.html
- apps/home/templates/etl.html
    ``add dynamic threshold alert``

## [1.8.1] - 2023-08-29
- fix/etl-bi [muhammad.muzakki@majoo.id]
### Changes
- apps/home/apis/etl_status_apis.py
    ``fix cockpit payload``

## [1.8.0] - 2023-08-29
- fix/etl-bi [muhammad.muzakki@majoo.id]
### Changes
- apps/home/apis/etl_apis.py
- apps/home/Models/etl_history.py
    ``add payment type transaction ETL``

## [1.7.0] - 2023-08-28
- fix/etl-bi [vera@majoo.id]
### Changes
- apps/home/apis/etl_apis.py
- apps/home/Models/etl_history.py
    ``add merchant transaction ETL``

## [1.6.3] - 2023-08-25
- fix/etl-bi [muhammad.muzakki@majoo.id]
### Changes
- apps/home/Models/etl_history.py
    ``update table name``

## [1.6.2] - 2023-08-21
- feature/report-status [muhammad.muzakki@majoo.id]
### Changes
- apps/home/apis/etl_status_apis.py
    ``fix sequence=0 after update data``

## [1.6.1] - 2023-08-21
- feature/recovery_promo [muhammad.muzakki@majoo.id]
### Changes
- apps/home/Models/recovery_history.py
    ``adjustment recovery promo model (table on datalake)``

## [1.6.0] - 2023-08-18
- feature/recovery_promo [muhammad.muzakki@majoo.id]
### Added
- apps/home/apis/recovery_promo_apis.py
- apps/static/assests/js/recoverypromo.js
- apps/templates/home/recovery_promo.html
### Changes
- apps/home/views.py
- apps/home/Models/recovery_history.py
- apps/templates/includes/sidebar.html
    ``add monitoring for recovery promo process``

## [1.5.1] - 2023-08-08
- adjustment/remove-old-etl [muhammad.muzakki@majoo.id]
### Changes
- apps/home/apis/dashboard.py
- apps/home/apis/etl_apis.py
- apps/home/Models/etl_history.py
    ``remove unused etl from monitoring and alert``

## [1.5.0] - 2023-08-08
- feature/report-status [muhammad.muzakki@majoo.id]
### Added
- apps/home/jobs/auto_switch.py
### Changes
- apps/home/scheduler.py
    ``automate process for switch datamart to non-datamart (vice versa)``

## [1.4.4] - 2023-08-08
- feature/report-status [muhammad.muzakki@majoo.id]
### Changes
- apps/templates/home/etl_status.html
- apps/templates/includes/sidebar.html
    ``added access for tac change the report status``

## [1.4.3] - 2023-08-08
- feature/report-status [muhammad.muzakki@majoo.id]
### Changes
- env.sample
- apps/home/urls.py
- apps/home/apis/etl_status.py
- apps/static/assets/js/etl_status.js
- apps/templates/home/etl_status.html
- core/settings.py
    ``added manual change for report status (datamart or non-datamart) and is_automate``

## [1.4.2] - 2023-08-02
- feature/report-status [muhammad.muzakki@majoo.id]
### Changes
- apps/home/apis/recovery_hard_delete.py
    ``fixed false flag for calculation waiting for recovery``

## [1.4.1] - 2023-08-02
- feature/report-status [muhammad.muzakki@majoo.id]
### Added
- apps/home/apis/etl_status_apis.py
- apps/home/static/js/etl_status.js
- apps/home/templates/home/etl_status.html
    ``added monitoring feature to control all of reporting on majoo dashboard``
### Changed
- apps/home/views.py
    ``added controller for etl status ``

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
