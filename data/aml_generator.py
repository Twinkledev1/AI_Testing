import random
import json
import uuid
from datetime import datetime, timedelta
from faker import Faker
import numpy as np

fake = Faker()

class AMLSyntheticDataGenerator:
    def __init__(self):
        self.transaction_types = [
            'WIRE_TRANSFER', 'ACH_TRANSFER', 'CASH_DEPOSIT', 'CASH_WITHDRAWAL',
            'CHECK_DEPOSIT', 'ATM_WITHDRAWAL', 'CARD_PAYMENT', 'ONLINE_TRANSFER',
            'MOBILE_PAYMENT', 'CRYPTOCURRENCY', 'MONEY_ORDER', 'TRAVELERS_CHECK'
        ]
        
        self.suspicious_patterns = [
            'STRUCTURING', 'ROUND_DOLLAR_AMOUNTS', 'RAPID_MOVEMENT', 'SMURFING',
            'LAYERING', 'UNUSUAL_VOLUME', 'HIGH_RISK_GEOGRAPHY', 'PEP_RELATED',
            'SANCTIONS_HIT', 'CASH_INTENSIVE', 'SHELL_COMPANY', 'TRADE_BASED'
        ]
        
        self.currencies = ['USD', 'EUR', 'GBP', 'CAD', 'JPY', 'AUD', 'CHF', 'CNY']
        self.countries = ['US', 'GB', 'DE', 'FR', 'CA', 'AU', 'JP', 'SG', 'CH', 'NL']
        self.high_risk_countries = ['AF', 'BY', 'CF', 'CG', 'IR', 'IQ', 'KP', 'LB', 'LY', 'MM', 'NI', 'SO', 'SS', 'SD', 'SY', 'VE', 'YE', 'ZW']
        
        self.banks = [
            'Chase Bank', 'Bank of America', 'Wells Fargo', 'Citibank', 'HSBC',
            'Deutsche Bank', 'Barclays', 'Credit Suisse', 'UBS', 'BNP Paribas'
        ]
        
        self.business_types = [
            'Money Service Business', 'Casino', 'Real Estate', 'Auto Dealership',
            'Jewelry Store', 'Art Gallery', 'Import/Export', 'Construction',
            'Restaurant', 'Technology', 'Consulting', 'Trading Company'
        ]
        
    def generate_transaction(self, customer_id=None, suspicious=False):
        """Generate a single transaction record"""
        transaction_id = str(uuid.uuid4())
        customer_id = customer_id or str(uuid.uuid4())
        
        # Base transaction
        base_amount = self._generate_transaction_amount(suspicious)
        transaction_date = fake.date_time_between(start_date='-90d', end_date='now')
        
        transaction = {
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'transaction_type': random.choice(self.transaction_types),
            'amount': base_amount,
            'currency': random.choice(self.currencies),
            'transaction_date': transaction_date.isoformat(),
            'originator': self._generate_party_info('originator'),
            'beneficiary': self._generate_party_info('beneficiary', suspicious),
            'intermediary_banks': self._generate_intermediary_banks(),
            'purpose_code': self._generate_purpose_code(),
            'description': fake.sentence(),
            'channel': random.choice(['ONLINE', 'BRANCH', 'ATM', 'MOBILE', 'PHONE', 'API']),
            'reference_number': fake.bothify('TXN-####-????-####'),
            'processing_status': random.choice(['COMPLETED', 'PENDING', 'FAILED', 'CANCELLED']),
            'aml_screening': self._generate_aml_screening(suspicious),
            'risk_indicators': self._generate_risk_indicators(suspicious),
            'compliance_flags': self._generate_compliance_flags(suspicious),
            'created_timestamp': datetime.now().isoformat()
        }
        
        return transaction
    
    def generate_suspicious_activity_report(self, customer_id, transactions):
        """Generate a Suspicious Activity Report (SAR)"""
        sar_id = str(uuid.uuid4())
        filing_date = fake.date_time_between(start_date='-30d', end_date='now')
        
        sar = {
            'sar_id': sar_id,
            'filing_institution': {
                'name': random.choice(self.banks),
                'routing_number': fake.aba(),
                'address': fake.address(),
                'contact_person': fake.name(),
                'phone': fake.phone_number()
            },
            'customer_id': customer_id,
            'suspect_information': self._generate_suspect_info(),
            'suspicious_activity_type': random.choice([
                'Money Laundering', 'Terrorist Financing', 'Fraud', 'Tax Evasion',
                'Sanctions Violations', 'Structuring', 'Identity Theft', 'Cyber Crime'
            ]),
            'activity_period': {
                'start_date': (filing_date - timedelta(days=90)).strftime('%Y-%m-%d'),
                'end_date': filing_date.strftime('%Y-%m-%d')
            },
            'total_amount_involved': sum([t['amount'] for t in transactions]),
            'currency': 'USD',
            'narrative_description': self._generate_narrative_description(transactions),
            'geographic_locations': self._get_geographic_locations(transactions),
            'filing_date': filing_date.strftime('%Y-%m-%d'),
            'filing_institution_contact': fake.name(),
            'law_enforcement_notification': random.choice([True, False]),
            'corrective_action_taken': fake.text(max_nb_chars=200),
            'status': random.choice(['DRAFT', 'FILED', 'UNDER_REVIEW', 'CLOSED']),
            'related_transactions': [t['transaction_id'] for t in transactions],
            'attachments': self._generate_sar_attachments(),
            'created_timestamp': datetime.now().isoformat()
        }
        
        return sar
    
    def _generate_transaction_amount(self, suspicious=False):
        """Generate transaction amounts with suspicious patterns"""
        if suspicious:
            # Generate amounts that might trigger AML alerts
            patterns = [
                lambda: 9999.99,  # Just under $10k reporting threshold
                lambda: round(random.uniform(9000, 9999), 2),  # Structuring pattern
                lambda: random.choice([5000, 7500, 10000, 15000, 25000]),  # Round amounts
                lambda: random.uniform(100000, 500000)  # Large amounts
            ]
            return random.choice(patterns)()
        else:
            # Normal transaction amounts with natural distribution
            return round(np.random.lognormal(mean=6, sigma=1.5), 2)
    
    def _generate_party_info(self, party_type, suspicious=False):
        """Generate originator or beneficiary information"""
        party = {
            'name': fake.name() if party_type == 'originator' else fake.company(),
            'account_number': fake.bban(),
            'routing_number': fake.aba(),
            'address': {
                'street': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'country': random.choice(self.high_risk_countries) if suspicious and random.random() < 0.3 else random.choice(self.countries),
                'postal_code': fake.postcode()
            },
            'bank_name': random.choice(self.banks),
            'swift_code': fake.swift(),
            'identification': {
                'type': random.choice(['SSN', 'PASSPORT', 'DRIVERS_LICENSE', 'TAX_ID']),
                'number': fake.ssn(),
                'issuing_country': random.choice(self.countries)
            }
        }
        
        if suspicious:
            # Add suspicious indicators
            party['pep_status'] = random.choice([True, False])
            party['sanctions_hit'] = random.choice([True, False]) if random.random() < 0.1 else False
            party['high_risk_customer'] = True
        
        return party
    
    def _generate_intermediary_banks(self):
        """Generate intermediary bank information"""
        if random.random() < 0.3:  # 30% chance of having intermediary banks
            return [
                {
                    'bank_name': random.choice(self.banks),
                    'swift_code': fake.swift(),
                    'country': random.choice(self.countries)
                }
                for _ in range(random.randint(1, 2))
            ]
        return []
    
    def _generate_purpose_code(self):
        """Generate purpose codes for transactions"""
        purpose_codes = [
            'SALA', 'PENS', 'SUPP', 'TRAD', 'TREA', 'LOAN', 'DIVI',
            'ROYLT', 'GOVN', 'SSBE', 'RLTI', 'INTC', 'OTHR'
        ]
        return random.choice(purpose_codes)
    
    def _generate_aml_screening(self, suspicious=False):
        """Generate AML screening results"""
        screening = {
            'sanctions_screening': {
                'status': 'HIT' if suspicious and random.random() < 0.2 else random.choice(['CLEAR', 'PENDING']),
                'lists_checked': ['OFAC_SDN', 'UN_1267', 'EU_SANCTIONS', 'HMT_SANCTIONS'],
                'match_score': random.randint(60, 100) if suspicious else random.randint(0, 30),
                'screening_timestamp': datetime.now().isoformat()
            },
            'pep_screening': {
                'status': 'HIT' if suspicious and random.random() < 0.15 else 'CLEAR',
                'match_score': random.randint(70, 100) if suspicious else random.randint(0, 20),
                'pep_category': random.choice(['DOMESTIC', 'FOREIGN', 'INTERNATIONAL']) if suspicious else None
            },
            'adverse_media': {
                'status': 'HIT' if suspicious and random.random() < 0.1 else 'CLEAR',
                'articles_found': random.randint(1, 5) if suspicious else 0,
                'risk_categories': ['FINANCIAL_CRIME', 'CORRUPTION', 'TERRORISM'] if suspicious else []
            }
        }
        
        return screening
    
    def _generate_risk_indicators(self, suspicious=False):
        """Generate risk indicators for transactions"""
        indicators = []
        
        if suspicious:
            # Add multiple suspicious indicators
            possible_indicators = [
                'UNUSUAL_TRANSACTION_PATTERN',
                'HIGH_VOLUME_LOW_VALUE',
                'RAPID_MOVEMENT_OF_FUNDS',
                'CASH_INTENSIVE_BUSINESS',
                'HIGH_RISK_GEOGRAPHY',
                'SHELL_COMPANY_INVOLVEMENT',
                'ROUND_DOLLAR_AMOUNTS',
                'STRUCTURING_PATTERN',
                'UNUSUAL_TIMING',
                'INCONSISTENT_BUSINESS_ACTIVITY'
            ]
            indicators = random.sample(possible_indicators, k=random.randint(2, 5))
        else:
            # Occasionally add minor indicators for normal transactions
            if random.random() < 0.1:
                indicators = [random.choice(['LARGE_AMOUNT', 'INTERNATIONAL_TRANSFER'])]
        
        return indicators
    
    def _generate_compliance_flags(self, suspicious=False):
        """Generate compliance flags and alerts"""
        flags = {
            'ctr_required': random.choice([True, False]) if random.random() < 0.05 else False,
            'sar_filed': suspicious and random.choice([True, False]),
            'enhanced_due_diligence': suspicious or random.choice([True, False]),
            'transaction_monitoring_alert': suspicious,
            'manual_review_required': suspicious or random.choice([True, False]),
            'regulatory_reporting': {
                'ctr_filed': random.choice([True, False]) if random.random() < 0.03 else False,
                'fbar_applicable': random.choice([True, False]) if random.random() < 0.02 else False,
                'form_8300_required': random.choice([True, False]) if random.random() < 0.01 else False
            }
        }
        
        return flags
    
    def _generate_suspect_info(self):
        """Generate suspect information for SAR"""
        return {
            'name': fake.name(),
            'account_numbers': [fake.bban() for _ in range(random.randint(1, 3))],
            'ssn_tin': fake.ssn(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'occupation': fake.job(),
            'relationship_to_institution': random.choice(['CUSTOMER', 'NON_CUSTOMER', 'EMPLOYEE', 'VENDOR'])
        }
    
    def _generate_narrative_description(self, transactions):
        """Generate narrative description for SAR"""
        patterns = [
            "Customer engaged in multiple transactions just under the reporting threshold, indicating possible structuring activity.",
            "Rapid movement of large sums through multiple accounts with no apparent business purpose.",
            "Customer's transaction patterns are inconsistent with their stated occupation and income level.",
            "Multiple wire transfers to high-risk jurisdictions without clear business justification.",
            "Unusual cash deposits followed immediately by wire transfers to foreign accounts."
        ]
        return random.choice(patterns)
    
    def _get_geographic_locations(self, transactions):
        """Extract geographic information from transactions"""
        locations = set()
        for tx in transactions:
            locations.add(tx['originator']['address']['country'])
            locations.add(tx['beneficiary']['address']['country'])
        return list(locations)
    
    def _generate_sar_attachments(self):
        """Generate SAR attachment information"""
        attachments = []
        attachment_types = ['ACCOUNT_STATEMENTS', 'TRANSACTION_RECORDS', 'CORRESPONDENCE', 'IDENTIFICATION_DOCS']
        
        for _ in range(random.randint(2, 5)):
            attachment = {
                'attachment_id': str(uuid.uuid4()),
                'type': random.choice(attachment_types),
                'filename': f"{random.choice(attachment_types).lower()}_{fake.uuid4()}.pdf",
                'file_size': random.randint(100, 5000),  # KB
                'upload_date': fake.date_time_between(start_date='-30d', end_date='now').isoformat()
            }
            attachments.append(attachment)
        
        return attachments
    
    def generate_transaction_pattern(self, pattern_type, customer_id, days=30):
        """Generate a series of transactions following a specific suspicious pattern"""
        transactions = []
        base_date = datetime.now() - timedelta(days=days)
        
        if pattern_type == 'STRUCTURING':
            # Generate multiple transactions just under $10,000
            for i in range(random.randint(5, 15)):
                amount = random.uniform(9000, 9999)
                tx_date = base_date + timedelta(days=random.randint(0, days))
                
                transaction = self.generate_transaction(customer_id, suspicious=True)
                transaction['amount'] = round(amount, 2)
                transaction['transaction_date'] = tx_date.isoformat()
                transaction['risk_indicators'].append('STRUCTURING_PATTERN')
                transactions.append(transaction)
        
        elif pattern_type == 'RAPID_MOVEMENT':
            # Generate quick succession of large transfers
            for i in range(random.randint(3, 8)):
                amount = random.uniform(50000, 500000)
                tx_date = base_date + timedelta(hours=i * random.randint(1, 6))
                
                transaction = self.generate_transaction(customer_id, suspicious=True)
                transaction['amount'] = round(amount, 2)
                transaction['transaction_date'] = tx_date.isoformat()
                transaction['risk_indicators'].append('RAPID_MOVEMENT_OF_FUNDS')
                transactions.append(transaction)
        
        elif pattern_type == 'SMURFING':
            # Generate multiple small transactions from different locations
            for i in range(random.randint(10, 25)):
                amount = random.uniform(500, 3000)
                tx_date = base_date + timedelta(days=random.randint(0, days))
                
                transaction = self.generate_transaction(customer_id, suspicious=True)
                transaction['amount'] = round(amount, 2)
                transaction['transaction_date'] = tx_date.isoformat()
                transaction['channel'] = random.choice(['ATM', 'BRANCH'])
                transaction['risk_indicators'].append('SMURFING_PATTERN')
                transactions.append(transaction)
        
        return transactions
    
    def generate_batch_transactions(self, customer_ids, count=1000, suspicious_ratio=0.1):
        """Generate a batch of transactions for multiple customers"""
        transactions = []
        suspicious_count = int(count * suspicious_ratio)
        normal_count = count - suspicious_count
        
        # Generate normal transactions
        for _ in range(normal_count):
            customer_id = random.choice(customer_ids)
            transaction = self.generate_transaction(customer_id, suspicious=False)
            transactions.append(transaction)
        
        # Generate suspicious transactions
        for _ in range(suspicious_count):
            customer_id = random.choice(customer_ids)
            transaction = self.generate_transaction(customer_id, suspicious=True)
            transactions.append(transaction)
        
        # Shuffle to mix normal and suspicious transactions
        random.shuffle(transactions)
        return transactions
    
    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Generated and saved data to {filename}")

# Example usage
if __name__ == "__main__":
    generator = AMLSyntheticDataGenerator()
    
    # Generate sample customer IDs
    customer_ids = [str(uuid.uuid4()) for _ in range(50)]
    
    # Generate batch of transactions
    transactions = generator.generate_batch_transactions(
        customer_ids=customer_ids,
        count=500,
        suspicious_ratio=0.15
    )
    
    # Save transactions
    generator.save_to_json(transactions, 'aml_synthetic_transactions.json')
    
    # Generate suspicious patterns
    structuring_pattern = generator.generate_transaction_pattern(
        'STRUCTURING', customer_ids[0], days=30
    )
    
    # Generate SAR report
    suspicious_transactions = [tx for tx in transactions if tx['risk_indicators']][:5]
    if suspicious_transactions:
        sar_report = generator.generate_suspicious_activity_report(
            customer_ids[0], suspicious_transactions
        )
        generator.save_to_json([sar_report], 'sample_sar_reports.json')
    
    print("\nSample Transaction:")
    print(json.dumps(transactions[0], indent=2))
    
    print(f"\nGenerated {len(transactions)} transactions")
    print(f"Suspicious transactions: {len([tx for tx in transactions if tx['risk_indicators']])}")
    print(f"Structuring pattern transactions: {len(structuring_pattern)}")