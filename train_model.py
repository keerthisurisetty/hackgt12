#!/usr/bin/env python3
"""
Clinic Cyber Attack Recovery ML Training Script
Trains machine learning models to predict recovery times for small clinics after cyber attacks
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ClinicRecoveryPredictor:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.best_model = None
        self.best_model_name = None
        self.feature_importance = None
        
    def generate_training_data(self, n_samples=150):
        """Generate realistic clinic cyber attack recovery data"""
        np.random.seed(42)  # For reproducibility
        
        # Clinic types and their characteristics
        clinic_types = ['solo_practice', 'small_group', 'medium_group']
        attack_types = ['phishing', 'ransomware', 'data_breach', 'malware', 'insider_threat']
        
        data = []
        
        for i in range(n_samples):
            # Generate clinic characteristics
            clinic_type = np.random.choice(clinic_types)
            
            if clinic_type == 'solo_practice':
                monthly_revenue = np.random.normal(25000, 5000)
                monthly_expenses = monthly_revenue * np.random.uniform(0.85, 0.95)
                staff_count = np.random.randint(2, 6)
                it_budget_pct = np.random.uniform(0.02, 0.05)
            elif clinic_type == 'small_group':
                monthly_revenue = np.random.normal(65000, 15000)
                monthly_expenses = monthly_revenue * np.random.uniform(0.80, 0.90)
                staff_count = np.random.randint(6, 15)
                it_budget_pct = np.random.uniform(0.03, 0.08)
            else:  # medium_group
                monthly_revenue = np.random.normal(120000, 25000)
                monthly_expenses = monthly_revenue * np.random.uniform(0.75, 0.85)
                staff_count = np.random.randint(15, 30)
                it_budget_pct = np.random.uniform(0.05, 0.12)
            
            # Ensure positive values
            monthly_revenue = max(15000, monthly_revenue)
            monthly_expenses = max(monthly_revenue * 0.7, monthly_expenses)
            
            # Financial ratios
            profit_margin = (monthly_revenue - monthly_expenses) / monthly_revenue
            cash_reserves = monthly_revenue * np.random.uniform(1.2, 3.5)
            operating_runway = cash_reserves / monthly_expenses
            
            # Attack characteristics
            attack_type = np.random.choice(attack_types)
            
            # Attack severity influences financial loss
            attack_severity_multipliers = {
                'phishing': np.random.uniform(0.5, 1.5),
                'ransomware': np.random.uniform(2.0, 4.0),
                'data_breach': np.random.uniform(1.5, 3.0),
                'malware': np.random.uniform(1.0, 2.5),
                'insider_threat': np.random.uniform(1.2, 2.8)
            }
            
            attack_severity = attack_severity_multipliers[attack_type]
            financial_loss = monthly_revenue * attack_severity * np.random.uniform(0.1, 0.8)
            
            # Security posture factors
            has_backup = np.random.choice([0, 1], p=[0.3, 0.7])
            has_incident_plan = np.random.choice([0, 1], p=[0.6, 0.4])
            has_cyber_insurance = np.random.choice([0, 1], p=[0.7, 0.3])
            security_training = np.random.choice([0, 1], p=[0.5, 0.5])
            
            # Recovery time calculation (our target variable)
            # Base recovery time influenced by multiple factors
            base_recovery_weeks = {
                'phishing': np.random.uniform(1, 3),
                'ransomware': np.random.uniform(3, 8),
                'data_breach': np.random.uniform(2, 6),
                'malware': np.random.uniform(2, 5),
                'insider_threat': np.random.uniform(2, 7)
            }[attack_type]
            
            # Factors that reduce recovery time
            recovery_time = base_recovery_weeks
            if has_backup: recovery_time *= 0.6
            if has_incident_plan: recovery_time *= 0.7
            if has_cyber_insurance: recovery_time *= 0.8
            if security_training: recovery_time *= 0.9
            
            # Financial factors
            if profit_margin > 0.15: recovery_time *= 0.8  # Good margins help
            if operating_runway > 60: recovery_time *= 0.7  # Good runway helps
            if it_budget_pct > 0.08: recovery_time *= 0.75  # Good IT investment helps
            
            # Size factors
            if staff_count > 20: recovery_time *= 1.2  # Larger orgs take longer
            
            # Add some noise and ensure reasonable bounds
            recovery_time *= np.random.uniform(0.8, 1.2)
            recovery_time = max(1, min(12, recovery_time))  # Between 1-12 weeks
            
            data.append({
                'clinic_type': clinic_type,
                'monthly_revenue': monthly_revenue,
                'monthly_expenses': monthly_expenses,
                'profit_margin': profit_margin,
                'cash_reserves': cash_reserves,
                'operating_runway': operating_runway,
                'staff_count': staff_count,
                'it_budget_pct': it_budget_pct,
                'attack_type': attack_type,
                'attack_severity': attack_severity,
                'financial_loss': financial_loss,
                'financial_loss_ratio': financial_loss / monthly_revenue,
                'has_backup': has_backup,
                'has_incident_plan': has_incident_plan,
                'has_cyber_insurance': has_cyber_insurance,
                'security_training': security_training,
                'recovery_weeks': recovery_time
            })
        
        return pd.DataFrame(data)
    
    def prepare_features(self, df):
        """Prepare features for ML training"""
        df_processed = df.copy()
        
        # Encode categorical variables
        le_clinic = LabelEncoder()
        le_attack = LabelEncoder()
        
        df_processed['clinic_type_encoded'] = le_clinic.fit_transform(df_processed['clinic_type'])
        df_processed['attack_type_encoded'] = le_attack.fit_transform(df_processed['attack_type'])
        
        # Store encoders
        self.encoders['clinic_type'] = le_clinic
        self.encoders['attack_type'] = le_attack
        
        # Select features for training
        feature_columns = [
            'monthly_revenue', 'monthly_expenses', 'profit_margin', 
            'cash_reserves', 'operating_runway', 'staff_count', 
            'it_budget_pct', 'attack_severity', 'financial_loss_ratio',
            'has_backup', 'has_incident_plan', 'has_cyber_insurance', 
            'security_training', 'clinic_type_encoded', 'attack_type_encoded'
        ]
        
        X = df_processed[feature_columns]
        y = df_processed['recovery_weeks']
        
        return X, y, feature_columns
    
    def train_models(self, X, y):
        """Train multiple ML models and compare performance"""
        print("🤖 Training ML Models for Clinic Recovery Prediction...")
        print("=" * 60)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['feature_scaler'] = scaler
        
        # Initialize models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\n📊 Training {name}...")
            
            # Train model
            if name == 'Linear Regression':
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            
            # Calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            # Cross validation
            if name == 'Linear Regression':
                cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='neg_mean_absolute_error')
            else:
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_absolute_error')
            
            cv_mae = -cv_scores.mean()
            
            results[name] = {
                'model': model,
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'cv_mae': cv_mae,
                'predictions': y_pred
            }
            
            print(f"   MAE: {mae:.2f} weeks")
            print(f"   RMSE: {rmse:.2f} weeks")
            print(f"   R²: {r2:.3f}")
            print(f"   CV MAE: {cv_mae:.2f} weeks")
        
        # Find best model
        best_model_name = min(results.keys(), key=lambda k: results[k]['cv_mae'])
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        self.models = results
        
        print(f"\n🏆 Best Model: {best_model_name}")
        print(f"   Cross-validation MAE: {results[best_model_name]['cv_mae']:.2f} weeks")
        
        # Feature importance for tree-based models
        if best_model_name in ['Random Forest', 'Gradient Boosting']:
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': self.best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            self.feature_importance = feature_importance
            
            print(f"\n📈 Top 5 Most Important Features:")
            for idx, row in feature_importance.head().iterrows():
                print(f"   {row['feature']}: {row['importance']:.3f}")
        
        return results, X_test, y_test
    
    def save_model(self, filename='clinic_recovery_model.joblib'):
        """Save the trained model and preprocessing objects"""
        model_package = {
            'model': self.best_model,
            'model_name': self.best_model_name,
            'scaler': self.scalers.get('feature_scaler'),
            'encoders': self.encoders,
            'feature_importance': self.feature_importance,
            'training_date': datetime.now().isoformat(),
            'model_metrics': {
                'mae': self.models[self.best_model_name]['mae'],
                'rmse': self.models[self.best_model_name]['rmse'],
                'r2': self.models[self.best_model_name]['r2'],
                'cv_mae': self.models[self.best_model_name]['cv_mae']
            }
        }
        
        joblib.dump(model_package, filename)
        print(f"\n💾 Model saved as: {filename}")
        return filename
    
    def predict_recovery(self, clinic_data):
        """Make predictions for new clinic data"""
        if self.best_model is None:
            raise ValueError("No trained model available. Run train_models() first.")
        
        # This would be used for real predictions
        # Implementation would depend on the input format
        pass

def main():
    """Main training pipeline"""
    print("🏥 Clinic Cyber Recovery ML Training Pipeline")
    print("=" * 50)
    
    # Initialize predictor
    predictor = ClinicRecoveryPredictor()
    
    # Generate training data
    print("\n📊 Generating training data...")
    df = predictor.generate_training_data(n_samples=200)
    print(f"Generated {len(df)} training samples")
    
    # Show data sample
    print(f"\n📋 Data Sample:")
    print(df[['clinic_type', 'attack_type', 'financial_loss_ratio', 'recovery_weeks']].head())
    
    # Prepare features
    X, y, feature_names = predictor.prepare_features(df)
    print(f"\n🔧 Features prepared: {len(feature_names)} features")
    
    # Train models
    results, X_test, y_test = predictor.train_models(X, y)
    
    # Save model
    model_file = predictor.save_model()
    
    # Generate sample predictions
    print(f"\n🎯 Sample Predictions:")
    print("-" * 30)
    
    sample_indices = np.random.choice(len(X_test), 3, replace=False)
    for i in sample_indices:
        actual = y_test.iloc[i]
        if predictor.best_model_name == 'Linear Regression':
            predicted = predictor.best_model.predict(predictor.scalers['feature_scaler'].transform(X_test.iloc[i:i+1]))[0]
        else:
            predicted = predictor.best_model.predict(X_test.iloc[i:i+1])[0]
        
        print(f"Actual: {actual:.1f} weeks | Predicted: {predicted:.1f} weeks | Error: {abs(actual-predicted):.1f} weeks")
    
    print(f"\n✅ Training Complete!")
    print(f"   Best Model: {predictor.best_model_name}")
    print(f"   Model saved: {model_file}")
    print(f"   Ready for integration with web app!")

if __name__ == "__main__":
    main()
