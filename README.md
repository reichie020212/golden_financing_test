# Test

### Install python3

	sudo apt install python3

### Install virtual environment

	sudo apt-get install python3-venv

### Create virtual environment

	python3 -m venv myvenv

### Activate virtual environment

	source myvenv/bin/activate

### Install Requirements

	python -m pip install --upgrade pip
	pip install -r requirements.txt

### Migrate

	python manage.py migrate

### Runserver

	python manage.py runserver

### Run in localhost

	Open localhost:8000 in your browser

### API
	Endpoints

	calculate loan: loan_calculator/ POST
		Sample Input:
			data = {
				'first_name': 'first_name_sample',
				'middle_name': 'middle_name_sample',
				'last_name': 'last_name_sample',
				'name_suffix': 'name_suffix_sample',
				'email': 'sample@sample.com',
				'phone_number': '+639266546598',
				'city': 'city_sample',
				'province': 'province_sample',
				'loan_type': 'type_a',
				'monthly_amortization': 0,
				'principal_amount': 10000,
				'loan_term': 12,
			}
			import requests
			r = requests.post(url='http://localhost:8000/loan_calculator/', json=data)
		Sample Output:
			[
				{
					'id': 18,
					'customer_info__first_name': 'first_name_sample',
					'customer_info__middle_name': 'middle_name_sample',
					'customer_info__last_name': 'last_name_sample',
					'customer_info__name_suffix': 'name_suffix_sample',
					'customer_info__email': 'sample@sample.com',
					'customer_info__phone_number': '+639266546598',
					'customer_info__city': 'city_sample',
					'customer_info__province': 'province_sample',
					'customer_info': 10,
					'loan_type': 'type_a',
					'principal_amount': 10000.0,
					'monthly_amortization': 945.6,
					'total_interest': 1347.2,
					'loan_term': 12,
					'total_sum_of_payments': 11347.2,
					'first_loan_payment_date': '2020-11-07',
					'loan_maturity_date': '2021-11-07'
			  	}
			]

	get list of all loan inquiries: loan_calculator/ GET
		Sample Input:
			r = requests.get(url='http://localhost:8000/loan_calculator/')
		Sample Output:
		    [
				{
					'customer_info__first_name': 'first_name_sample',
					'customer_info__middle_name': 'middle_name_sample',
					'customer_info__last_name': 'last_name_sample',
					'customer_info__name_suffix': 'name_suffix_sample',
					'customer_info__email': 'sample@sample.com',
					'customer_info__phone_number': '+639266546598',
					'customer_info__city': 'city_sample',
					'customer_info__province': 'province_sample',
					'customer_info': 11,
					'loan_type': 'type_a',
					'principal_amount': 10000.0,
					'monthly_amortization': 945.6,
					'total_interest': 1347.2,
					'loan_term': 12,
					'total_sum_of_payments': 11347.2,
					'first_loan_payment_date': '2020-11-07',
					'loan_maturity_date': '2021-11-07'
			  	}
			]

	get list of loan inquries by product type: loan_calculator/?loan_type=<type_a or type_b> GET
		Sample Input:
			r = requests.get(url='http://localhost:8000/loan_calculator/?loan_type=type_a')
		Sample Output:
		    [
				{
					'customer_info__first_name': 'first_name_sample',
					'customer_info__middle_name': 'middle_name_sample',
					'customer_info__last_name': 'last_name_sample',
					'customer_info__name_suffix': 'name_suffix_sample',
					'customer_info__email': 'sample@sample.com',
					'customer_info__phone_number': '+639266546598',
					'customer_info__city': 'city_sample',
					'customer_info__province': 'province_sample',
					'customer_info': 11,
					'loan_type': 'type_a',
					'principal_amount': 10000.0,
					'monthly_amortization': 945.6,
					'total_interest': 1347.2,
					'loan_term': 12,
					'total_sum_of_payments': 11347.2,
					'first_loan_payment_date': '2020-11-07',
					'loan_maturity_date': '2021-11-07'
			  	}
			]
