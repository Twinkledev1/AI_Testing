import pytest
import json

class TestAML:
    @pytest.fixture
    def aml_data(self):
        with open('synthetic_data/aml_data.json', 'r') as f:
            return json.load(f)
    
    def test_transaction_monitoring(self, aml_data):
        """TC-AML-001: Verify transaction monitoring thresholds"""
        for txn in aml_data:
            if txn['amount'] >= 10000:
                assert txn['flag'] in ['high_risk', 'suspicious']
    
    def test_suspicious_patterns(self, aml_data):
        """TC-AML-002: Detect suspicious transaction patterns"""
        suspicious_indicators = ['offshore_account', 'cash_deposit']
        for txn in aml_data:
            if any(ind in str(txn.values()) for ind in suspicious_indicators):
                assert txn['flag'] != 'normal'
    
    def test_reporting_requirements(self, aml_data):
        """TC-AML-003: Verify SAR/CTR report generation"""
        report_required = []
        for txn in aml_data:
            if txn['flag'] == 'suspicious' or txn['amount'] >= 10000:
                report_required.append(txn['transaction_id'])
        assert len(report_required) >= 2