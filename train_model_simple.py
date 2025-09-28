#!/usr/bin/env python3
"""
Simplified Clinic Recovery ML Training Script
Creates a trained model file for the hackathon demo
"""

import json
import pickle
import random
import math
from datetime import datetime

class SimpleClinicRecoveryModel:
    def __init__(self):
        self.model_weights = {}
        self.training_data = []
        self.model_stats = {}
        
    def generate_training_data(self, n_samples=100):
        """Generate realistic clinic recovery training data"""
        random.seed(42)  # For reproducibility
        
        clinic_types = ['solo_practice', 'small_group', 'medium_group']
        attack_types = ['phishing', 'ransomware', 'data_breach', 'malware']
        
        data = []
        
        for i in range(n_samples):
            # Generate clinic characteristics
            clinic_type = random.choice(clinic_types)
            
            if clinic_type == 'solo_practice':
                monthly_revenue = random.uniform(20000, 35000)
                staff_count = random.randint(2, 5)
                it_maturity = random.uniform(0.2, 0.6)
            elif clinic_type == 'small_group':
                monthly_revenue = random.uniform(50000, 80000)
                staff_count = random.randint(6, 15)
                it_maturity = random.uniform(0.4, 0.7)
            else:  # medium_group
                monthly_revenue = random.uniform(100000, 150000)
                staff_count = random.randint(15, 30)
                it_maturity = random.uniform(0.6, 0.9)
            
            monthly_expenses = monthly_revenue * random.uniform(0.75, 0.95)
            cash_reserves = monthly_revenue * random.uniform(1.5, 4.0)
            
            # Attack characteristics
            attack_type = random.choice(attack_types)
            financial_loss = monthly_revenue * random.uniform(0.1, 0.8)
            
            # Security posture
            has_backup = random.choice([True, False])
            has_incident_plan = random.choice([True, False])
            has_insurance = random.choice([True, False])
            
            # Calculate recovery time (target variable)
            base_weeks = {
                'phishing': random.uniform(1, 3),
                'ransomware': random.uniform(4, 8),
                'data_breach': random.uniform(2, 6),
                'malware': random.uniform(2, 5)
            }[attack_type]
            
            # Apply modifiers
            recovery_weeks = base_weeks
            if has_backup: recovery_weeks *= 0.7
            if has_incident_plan: recovery_weeks *= 0.8
            if has_insurance: recovery_weeks *= 0.9
            if it_maturity > 0.7: recovery_weeks *= 0.8
            if staff_count > 20: recovery_weeks *= 1.2
            
            # Ensure reasonable bounds
            recovery_weeks = max(1, min(12, recovery_weeks))
            
            record = {
                'clinic_type': clinic_type,
                'monthly_revenue': monthly_revenue,
                'monthly_expenses': monthly_expenses,
                'cash_reserves': cash_reserves,
                'staff_count': staff_count,
                'it_maturity': it_maturity,
                'attack_type': attack_type,
                'financial_loss': financial_loss,
                'financial_loss_ratio': financial_loss / monthly_revenue,
                'has_backup': has_backup,
                'has_incident_plan': has_incident_plan,
                'has_insurance': has_insurance,
                'recovery_weeks': recovery_weeks
            }
            
            data.append(record)
        
        self.training_data = data
        return data
    
    def train_model(self):
        """Train a simple linear model using the generated data"""
        print("🤖 Training Clinic Recovery Prediction Model...")
        print("=" * 50)
        
        if not self.training_data:
            raise ValueError("No training data available")
        
        # Calculate feature weights based on correlation analysis
        # This simulates what a real ML model would learn
        
        attack_weights = {}
        clinic_weights = {}
        
        # Analyze attack type impact
        for attack in ['phishing', 'ransomware', 'data_breach', 'malware']:
            attack_recoveries = [d['recovery_weeks'] for d in self.training_data if d['attack_type'] == attack]
            attack_weights[attack] = sum(attack_recoveries) / len(attack_recoveries)
        
        # Analyze clinic type impact  
        for clinic in ['solo_practice', 'small_group', 'medium_group']:
            clinic_recoveries = [d['recovery_weeks'] for d in self.training_data if d['clinic_type'] == clinic]
            clinic_weights[clinic] = sum(clinic_recoveries) / len(clinic_recoveries)
        
        # Calculate feature importance
        financial_impact = sum([d['financial_loss_ratio'] * d['recovery_weeks'] for d in self.training_data]) / len(self.training_data)
        backup_impact = sum([d['recovery_weeks'] for d in self.training_data if not d['has_backup']]) / max(1, len([d for d in self.training_data if not d['has_backup']]))
        
        self.model_weights = {
            'attack_weights': attack_weights,
            'clinic_weights': clinic_weights,
            'financial_impact_factor': financial_impact,
            'backup_reduction': 0.3,
            'incident_plan_reduction': 0.2,
            'insurance_reduction': 0.1,
            'it_maturity_factor': 0.25
        }
        
        # Calculate model performance stats
        predictions = []
        actuals = []
        
        for record in self.training_data:
            predicted = self.predict_recovery_time(record)
            predictions.append(predicted)
            actuals.append(record['recovery_weeks'])
        
        # Calculate Mean Absolute Error
        mae = sum(abs(p - a) for p, a in zip(predictions, actuals)) / len(predictions)
        
        # Calculate R-squared
        mean_actual = sum(actuals) / len(actuals)
        ss_res = sum((a - p) ** 2 for a, p in zip(actuals, predictions))
        ss_tot = sum((a - mean_actual) ** 2 for a in actuals)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        self.model_stats = {
            'mae': mae,
            'r_squared': r_squared,
            'training_samples': len(self.training_data),
            'mean_recovery_weeks': mean_actual
        }
        
        print(f"📊 Model Training Results:")
        print(f"   Training Samples: {len(self.training_data)}")
        print(f"   Mean Absolute Error: {mae:.2f} weeks")
        print(f"   R-squared: {r_squared:.3f}")
        print(f"   Average Recovery Time: {mean_actual:.1f} weeks")
        
        return self.model_weights, self.model_stats
    
    def predict_recovery_time(self, clinic_data):
        """Predict recovery time for a clinic scenario"""
        if not self.model_weights:
            raise ValueError("Model not trained yet")
        
        # Base prediction from attack type
        base_time = self.model_weights['attack_weights'].get(clinic_data['attack_type'], 4.0)
        
        # Adjust for clinic type
        clinic_factor = self.model_weights['clinic_weights'].get(clinic_data['clinic_type'], 1.0) / 4.0
        
        # Apply financial impact
        financial_factor = 1 + (clinic_data['financial_loss_ratio'] * 0.5)
        
        # Apply security posture adjustments
        security_factor = 1.0
        if clinic_data.get('has_backup'): security_factor -= self.model_weights['backup_reduction']
        if clinic_data.get('has_incident_plan'): security_factor -= self.model_weights['incident_plan_reduction']
        if clinic_data.get('has_insurance'): security_factor -= self.model_weights['insurance_reduction']
        
        # IT maturity factor
        it_factor = 1.0 - (clinic_data.get('it_maturity', 0.5) * self.model_weights['it_maturity_factor'])
        
        predicted_time = base_time * clinic_factor * financial_factor * security_factor * it_factor
        
        return max(1.0, min(12.0, predicted_time))
    
    def save_model(self, filename='clinic_recovery_model.json'):
        """Save the trained model to a file"""
        model_package = {
            'model_type': 'SimpleClinicRecovery',
            'version': '1.0',
            'training_date': datetime.now().isoformat(),
            'model_weights': self.model_weights,
            'model_stats': self.model_stats,
            'feature_list': [
                'clinic_type', 'attack_type', 'financial_loss_ratio',
                'has_backup', 'has_incident_plan', 'has_insurance', 'it_maturity'
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(model_package, f, indent=2)
        
        print(f"💾 Model saved as: {filename}")
        return filename

def main():
    """Main training pipeline"""
    print("🏥 Clinic Cyber Recovery ML Training")
    print("=" * 40)
    
    # Initialize model
    model = SimpleClinicRecoveryModel()
    
    # Generate training data
    print("\n📊 Generating training data...")
    training_data = model.generate_training_data(n_samples=150)
    print(f"Generated {len(training_data)} training samples")
    
    # Show sample data
    print("\n📋 Sample Training Records:")
    for i in range(3):
        record = training_data[i]
        print(f"   {record['clinic_type']} | {record['attack_type']} | "
              f"Loss: ${record['financial_loss']:.0f} | Recovery: {record['recovery_weeks']:.1f} weeks")
    
    # Train model
    weights, stats = model.train_model()
    
    # Save model
    model_file = model.save_model()
    
    # Test predictions
    print(f"\n🎯 Sample Predictions:")
    print("-" * 30)
    
    test_cases = [
        {
            'clinic_type': 'solo_practice',
            'attack_type': 'ransomware',
            'financial_loss_ratio': 0.3,
            'has_backup': True,
            'has_incident_plan': False,
            'has_insurance': True,
            'it_maturity': 0.4
        },
        {
            'clinic_type': 'small_group',
            'attack_type': 'phishing',
            'financial_loss_ratio': 0.1,
            'has_backup': False,
            'has_incident_plan': True,
            'has_insurance': False,
            'it_maturity': 0.6
        }
    ]
    
    for i, case in enumerate(test_cases):
        prediction = model.predict_recovery_time(case)
        print(f"Test {i+1}: {case['clinic_type']} + {case['attack_type']} = {prediction:.1f} weeks")
    
    print(f"\n✅ Training Complete!")
    print(f"   Model Performance: MAE = {stats['mae']:.2f} weeks")
    print(f"   Model saved: {model_file}")
    print(f"   Ready for web app integration!")

if __name__ == "__main__":
    main()