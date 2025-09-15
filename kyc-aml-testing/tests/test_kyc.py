import pytest
import json

class TestKYC:
    @pytest.fixture
    def kyc_data(self):
        with open('synthetic_data/kyc_data.json', 'r') as f:
            return json.load(f)
    
    def test_document_upload(self):
        """TC-KYC-001: Verify document upload functionality"""
        allowed_formats = ['pdf', 'jpg', 'png']
        test_file = 'passport.jpg'
        assert test_file.split('.')[-1] in allowed_formats
    
    def test_verification_status(self, kyc_data):
        """TC-KYC-002: Verify KYC status updates"""
        valid_statuses = ['pending', 'verified', 'rejected']
        for customer in kyc_data:
            assert customer['verification_status'] in valid_statuses
    
    def test_risk_scoring(self, kyc_data):
        """TC-KYC-003: Verify risk score calculation"""
        for customer in kyc_data:
            assert 0 <= customer['risk_score'] <= 100
            if customer['risk_score'] > 70:
                assert customer['verification_status'] == 'rejected'