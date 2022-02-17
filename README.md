# Adjust Performance Metric Monitoring

## About
This API is an interface for a sample dataset. You can retrieve a single row or list rows by query parameters.

## Installation
Python 3.8 or newer is required.
```
pip install -r requirements.txt
```
To run
```
python manage.py runserver
```

## Usage

You can filter, order, group, aggregate data by using query parameters with 1 end point. 
```
http://localhost:8000/api/v1/performance_metrics/
```

<i>/api/v1/performance_metrics</i> is the only end point you need to perform complex queries on performance_metrics table.

# Query Parameter Structure
## Selecting Columns
You can select the columns/fields that you want to fetch from db by using query parameter "column". You should use query parameter multiple times to assign multiple parameters to it.
<br>
<b>Example</b>
```
http://localhost:8000/api/v1/performance_metrics/?column=channel&column=os&column=date
```

## Filter / Search

Columns of dataset table are : <b>date	| channel	| country |	os |	impressions |	clicks |	installs |	spend |	revenue </b>
<br>You can filter any of these columns by using django orm lookups (guide link: https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups)<br>
<b>Example</b>
```
http://localhost:8000/api/v1/performance_metrics/?os=ios
http://localhost:8000/api/v1/performance_metrics/?clicks__gte=1000
```
## Ordering
You can order data by any column ( this could be limited by columns like clicks, installs, spend and revenue) by declaring <i>ordering</i> parameter in query params. For descending order add (-) to field.
<br>
<b>Example</b>
```
http://localhost:8000/api/v1/performance_metrics/?ordering=-clicks
```

## AGGREGATION
You can use aggregation functions like Sum and Count by passing query parameter (sum=(field), count=(field)).
## Grouping
You can group your data by adding group_by query param. You can use this parameter multiple times to group 1 or more fields.
<br>
<b>Example</b>
```
http://localhost:8000/api/v1/performance_metrics/?ordering=-click&sum=clicks&date__lte=2017-06-01&group_by=clicks&sum=impressions&group_by=channel&group_by=country
```
## Special Cases
### CPI Metric
You can get cpi (cost per install) metric by passing get_cpi=True query param.
### Date Ranges
You can specify start_date as date__gte and end date as date__lte

## Common API use-cases
### 1. To Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order
````
```
http://localhost:8000/api/v1/performance_metrics/?ordering=-clicks&group_by=channel&group_by=country&date__lte=2017-06-01&column=clicks&sum=clicks&column=impressions&sum=impressions
```
````

### 2. To Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
```
http://localhost:8000/api/v1/performance_metrics/?ordering=date&group_by=date&sum=installs&date__gte=2017-05-01&os=ios&date__lte=2017-05-31&column=os
```

### 3. To Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
```
http://localhost:8000/api/v1/performance_metrics/?ordering=-revenue&group_by=revenue&date=2017-06-01&group_by=os
```

### 4. To Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order:
```
http://localhost:8000/api/v1/performance_metrics/?ordering=-cpi&get_cpi=True&column=cpi&country=CA&column=country
```
