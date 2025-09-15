import random
import json
from datetime import datetime, timedelta
from faker import Faker
import uuid

# Initialize Faker for different locales
fake_us = Faker('en_US')
fake_uk = Faker('en_GB')
fake_de = Faker('de_DE')
fake_fr = Faker('fr_FR')

class KYCSyntheticDataGenerator:
    def __init__(self):
        self.risk_levels = ['LOW', 'MEDIUM', 'HIGH']
        self.document_types = ['PASSPORT', 'DRIVERS_LICENSE', 'NATIONAL_ID', 'UTILITY_BILL', 'BANK_STATEMENT']
        self.customer_types = ['INDIVIDUAL', 'BUSINESS']
        self.account_types = ['CHECKING', 'SAVINGS', 'BUSINESS', 'INVESTMENT']
        self.countries = ['US', 'GB', 'DE', 'FR', 'CA', 'AU', 'JP', 'SG']
        self.industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Government']
        
    def generate_individual_customer(self, locale='us'):
        """Generate synthetic data for individual customer"""
        faker_instance = self._get_faker_instance(locale)
        
        customer_id = str(uuid.uuid4())
        birth_date = faker_instance.date_of_birth(minimum_age=18, maximum_age=85)
        
        customer_data = {
            'customer_id': customer_id,
            'customer_type': 'INDIVIDUAL',
            'personal_info': {
                'first_name': faker_instance.first_name(),
                'last_name': faker_instance.last_name(),
                'middle_name': faker_instance.first_name() if random.choice([True, False]) else None,
                'date_of_birth': birth_date.strftime('%Y-%m-%d'),
                'gender': random.choice(['M', 'F', 'OTHER']),
                'nationality': self._get_nationality_by_locale(locale),
                'place_of_birth': faker_instance.city(),
                'marital_status': random.choice(['SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED'])
            },
            'contact_info': {
                'email': faker_instance.email(),
                'phone_primary': faker_instance.phone_number(),
                'phone_secondary': faker_instance.phone_number() if random.choice([True, False]) else None,
                'address': {
                    'street': faker_instance.street_address(),
                    'city': faker_instance.city(),
                    'state': faker_instance.state(),
                    'postal_code': faker_instance.postcode(),
                    'country': self._get_country_by_locale(locale)
                }
            },
            'employment_info': {
                'employment_status': random.choice(['EMPLOYED', 'SELF_EMPLOYED', 'UNEMPLOYED', 'RETIRED', 'STUDENT']),
                'employer_name': faker_instance.company() if random.choice([True, False, True]) else None,
                'job_title': faker_instance.job(),
                'annual_income': random.randint(25000, 500000),
                'industry': random.choice(self.industries)
            },
            'identification_documents': self._generate_identification_documents(),
            'risk_assessment': {
                'risk_level': random.choice(self.risk_levels),
                'risk_score': random.randint(1, 100),
                'pep_status': random.choice([True, False]) if random.random() < 0.05 else False,
                'sanctions_check': random.choice(['CLEAR', 'PENDING', 'HIT']) if random.random() < 0.02 else 'CLEAR',
                'adverse_media': random.choice([True, False]) if random.random() < 0.03 else False
            },
            'account_info': {
                'account_type': random.choice(self.account_types),
                'opening_balance': random.randint(100, 10000),
                'monthly_transaction_limit': random.randint(5000, 50000),
                'purpose_of_account': random.choice(['PERSONAL_BANKING', 'BUSINESS_BANKING', 'INVESTMENT', 'SAVINGS'])
            },
            'kyc_status': {
                'status': random.choice(['PENDING', 'IN_PROGRESS', 'APPROVED', 'REJECTED', 'REQUIRES_ADDITIONAL_INFO']),
                'submission_date': faker_instance.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
                'completion_date': faker_instance.date_between(start_date='-20d', end_date='today').strftime('%Y-%m-%d') if random.choice([True, False]) else None,
                'assigned_analyst': faker_instance.name(),
                'notes': faker_instance.text(max_nb_chars=200) if random.choice([True, False]) else None
            },
            'created_timestamp': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        return customer_data
    
    def generate_business_customer(self, locale='us'):
        """Generate synthetic data for business customer"""
        faker_instance = self._get_faker_instance(locale)
        
        customer_id = str(uuid.uuid4())
        registration_date = faker_instance.date_between(start_date='-10y', end_date='-1y')
        
        customer_data = {
            'customer_id': customer_id,
            'customer_type': 'BUSINESS',
            'business_info': {
                'legal_name': faker_instance.company(),
                'trading_name': faker_instance.company() if random.choice([True, False]) else None,
                'registration_number': faker_instance.ssn().replace('-', ''),
                'tax_id': faker_instance.ssn(),
                'registration_date': registration_date.strftime('%Y-%m-%d'),
                'business_type': random.choice(['CORPORATION', 'LLC', 'PARTNERSHIP', 'SOLE_PROPRIETORSHIP']),
                'industry': random.choice(self.industries),
                'nature_of_business': faker_instance.bs(),
                'number_of_employees': random.randint(1, 1000),
                'annual_revenue': random.randint(100000, 50000000)
            },
            'registered_address': {
                'street': faker_instance.street_address(),
                'city': faker_instance.city(),
                'state': faker_instance.state(),
                'postal_code': faker_instance.postcode(),
                'country': self._get_country_by_locale(locale)
            },
            'operating_address': {
                'street': faker_instance.street_address(),
                'city': faker_instance.city(),
                'state': faker_instance.state(),
                'postal_code': faker_instance.postcode(),
                'country': self._get_country_by_locale(locale)
            },
            'authorized_signatories': [
                {
                    'name': faker_instance.name(),
                    'title': random.choice(['CEO', 'CFO', 'Director', 'Partner']),
                    'date_of_birth': faker_instance.date_of_birth(minimum_age=25, maximum_age=70).strftime('%Y-%m-%d'),
                    'nationality': self._get_nationality_by_locale(locale),
                    'ownership_percentage': random.randint(10, 100) if random.choice([True, False]) else None
                }
                for _ in range(random.randint(1, 3))
            ],
            'beneficial_owners': [
                {
                    'name': faker_instance.name(),
                    'date_of_birth': faker_instance.date_of_birth(minimum_age=25, maximum_age=70).strftime('%Y-%m-%d'),
                    'nationality': self._get_nationality_by_locale(locale),
                    'ownership_percentage': random.randint(25, 100),
                    'pep_status': random.choice([True, False]) if random.random() < 0.1 else False
                }
                for _ in range(random.randint(1, 4))
            ],
            'identification_documents': self._generate_business_documents(),
            'risk_assessment': {
                'risk_level': random.choice(self.risk_levels),
                'risk_score': random.randint(1, 100),
                'high_risk_jurisdiction': random.choice([True, False]) if random.random() < 0.1 else False,
                'sanctions_check': random.choice(['CLEAR', 'PENDING', 'HIT']) if random.random() < 0.05 else 'CLEAR',
                'adverse_media': random.choice([True, False]) if random.random() < 0.08 else False
            },
            'account_info': {
                'account_type': 'BUSINESS',
                'opening_balance': random.randint(10000, 1000000),
                'monthly_transaction_limit': random.randint(100000, 5000000),
                'purpose_of_account': random.choice(['BUSINESS_OPERATIONS', 'PAYROLL', 'INVESTMENT', 'TREASURY'])
            },
            'kyc_status': {
                'status': random.choice(['PENDING', 'IN_PROGRESS', 'APPROVED', 'REJECTED', 'REQUIRES_ADDITIONAL_INFO']),
                'submission_date': faker_instance.date_between(start_date='-60d', end_date='today').strftime('%Y-%m-%d'),
                'completion_date': faker_instance.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d') if random.choice([True, False]) else None,
                'assigned_analyst': faker_instance.name(),
                'notes': faker_instance.text(max_nb_chars=200) if random.choice([True, False]) else None
            },
            'created_timestamp': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        return customer_data
    
    def _generate_identification_documents(self):
        """Generate identification documents for individual customers"""
        documents = []
        doc_count = random.randint(2, 4)
        selected_docs = random.sample(self.document_types, doc_count)
        
        for doc_type in selected_docs:
            doc = {
                'document_id': str(uuid.uuid4()),
                'document_type': doc_type,
                'document_number': fake_us.ssn() if doc_type == 'PASSPORT' else fake_us.license_plate(),
                'issuing_authority': fake_us.company(),
                'issue_date': fake_us.date_between(start_date='-10y', end_date='-1y').strftime('%Y-%m-%d'),
                'expiry_date': fake_us.date_between(start_date='today', end_date='+10y').strftime('%Y-%m-%d'),
                'issuing_country': random.choice(self.countries),
                'verification_status': random.choice(['VERIFIED', 'PENDING', 'REJECTED', 'EXPIRED']),
                'file_path': f"/documents/{doc_type.lower()}_{fake_us.uuid4()}.pdf"
            }
            documents.append(doc)
        
        return documents
    
    def _generate_business_documents(self):
        """Generate business documents"""
        business_docs = ['CERTIFICATE_OF_INCORPORATION', 'MEMORANDUM_OF_ASSOCIATION', 'TAX_CERTIFICATE', 'BANK_STATEMENT', 'UTILITY_BILL']
        documents = []
        
        for doc_type in business_docs:
            doc = {
                'document_id': str(uuid.uuid4()),
                'document_type': doc_type,
                'document_number': fake_us.ssn().replace('-', ''),
                'issuing_authority': fake_us.company() if 'CERTIFICATE' in doc_type else 'Tax Authority',
                'issue_date': fake_us.date_between(start_date='-5y', end_date='-1m').strftime('%Y-%m-%d'),
                'expiry_date': fake_us.date_between(start_date='today', end_date='+5y').strftime('%Y-%m-%d') if random.choice([True, False]) else None,
                'issuing_country': random.choice(self.countries[:3]),  # Limit to major countries
                'verification_status': random.choice(['VERIFIED', 'PENDING', 'REJECTED']),
                'file_path': f"/documents/business_{doc_type.lower()}_{fake_us.uuid4()}.pdf"
            }
            documents.append(doc)
        
        return documents
    
    def _get_faker_instance(self, locale):
        """Return appropriate Faker instance based on locale"""
        locale_map = {
            'us': fake_us,
            'uk': fake_uk,
            'de': fake_de,
            'fr': fake_fr
        }
        return locale_map.get(locale, fake_us)
    
    def _get_nationality_by_locale(self, locale):
        """Get nationality based on locale"""
        nationality_map = {
            'us': 'American',
            'uk': 'British',
            'de': 'German',
            'fr': 'French'
        }
        return nationality_map.get(locale, 'American')
    
    def _get_country_by_locale(self, locale):
        """Get country code based on locale"""
        country_map = {
            'us': 'US',
            'uk': 'GB',
            'de': 'DE',
            'fr': 'FR'
        }
        return country_map.get(locale, 'US')
    
    def generate_batch_customers(self, count=100, individual_ratio=0.8):
        """Generate a batch of customers with specified individual/business ratio"""
        customers = []
        individual_count = int(count * individual_ratio)
        business_count = count - individual_count
        
        # Generate individual customers
        for _ in range(individual_count):
            locale = random.choice(['us', 'uk', 'de', 'fr'])
            customers.append(self.generate_individual_customer(locale))
        
        # Generate business customers
        for _ in range(business_count):
            locale = random.choice(['us', 'uk', 'de'])
            customers.append(self.generate_business_customer(locale))
        
        return customers
    
    def save_to_json(self, customers, filename):
        """Save customers data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(customers, f, indent=2, ensure_ascii=False)
        print(f"Generated {len(customers)} customer records and saved to {filename}")

# Example usage
if __name__ == "__main__":
    generator = KYCSyntheticDataGenerator()
    
    # Generate sample customers
    customers = generator.generate_batch_customers(count=50, individual_ratio=0.7)
    
    # Save to file
    generator.save_to_json(customers, 'kyc_synthetic_customers.json')
    
    # Print sample customer for review
    print("\nSample Individual Customer:")
    print(json.dumps([c for c in customers if c['customer_type'] == 'INDIVIDUAL'][0], indent=2))
    
    print("\nSample Business Customer:")
    business_customers = [c for c in customers if c['customer_type'] == 'BUSINESS']
    if business_customers:
        print(json.dumps(business_customers[0], indent=2))