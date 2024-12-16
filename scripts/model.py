import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error
import joblib
import os

class DASSModel:
    def __init__(self):
        self.logistic_model = None
        self.linear_model = None
        self.load_model()

    def train_and_save_model(self):
        # Load dataset (replace with actual data path)
        df = pd.read_excel('dataset.xlsx')

        # Drop unnecessary columns
        columns_to_drop = ['Timestamp', 'Email Address', 'Name (optional)', 'Email Address', 'Grade Level', 'Modality', 'Strand']
        df.drop(columns=columns_to_drop, inplace=True)

        # Convert categorical responses to numerical scores
        conversion_dict = {
            'Never': 0, 'Sometimes': 1, 'Often': 2, 'Very Often': 3
        }
        columns_to_convert = [
            'I couldn’t seem to experience any positive feelings at all', 'I found it difficult to work up the initiative to do things',
            'I felt that I had nothing to look forward to', 'I was downhearted and blue', 'I was unable to become enthusiastic about anything',
            'I feel like I am not worth anything as a person', 'I believe that life is meaningless', 'I was aware of the dryness of my mouth',
            'I experienced breathing difficulty (e.g. excessively rapid breathing, breathless in the absence of physical exertion)',
            'I experienced trembling (e.g. in the hands)', 'I felt I was close to panic', 'I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat',
            'I felt scared without any good reason', 'I found it hard to wind down', 'I tend to overreact to small-scale circumstances',
            'I felt like I was using a lot of nervous energy', 'I found myself getting more agitated', 'I found it more difficult to relax',
            'I was intolerant of anything that kept me from getting on what I was doing', 'I felt that I was rather touchy'
        ]
        df[columns_to_convert] = df[columns_to_convert].replace(conversion_dict)

        # Define DASS-21 Question categories
        depression_questions = [
            'I felt that I had nothing to look forward to', 'I was unable to become enthusiastic about anything',
            'I feel like I am not worth anything as a person', 'I believe that life is meaningless',
            'I couldn’t seem to experience any positive feelings at all', 'I found it difficult to work up the initiative to do things',
            'I was downhearted and blue'
        ]
        anxiety_questions = [
            'I was aware of the dryness of my mouth', 'I experienced breathing difficulty (e.g. excessively rapid breathing, breathless in the absence of physical exertion)',
            'I experienced trembling (e.g. in the hands)', 'I felt I was close to panic',
            'I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat',
            'I felt scared without any good reason'
        ]
        stress_questions = [
            'I found it hard to wind down', 'I tend to overreact to small-scale circumstances', 'I felt like I was using a lot of nervous energy',
            'I found myself getting more agitated', 'I found it more difficult to relax', 'I was intolerant of anything that kept me from getting on what I was doing',
            'I felt that I was rather touchy'
        ]

        # Compute DASS-21 Scores
        df['Depression'] = df[depression_questions].sum(axis=1) * 2
        df['Anxiety'] = df[anxiety_questions].sum(axis=1) * 2
        df['Stress'] = df[stress_questions].sum(axis=1) * 2

        # Define Target Variables
        df['Depression_Increase'] = (df['Depression'] > 13).astype(int)  # Binary Target
        df['Depression_Increase_Magnitude'] = df['Depression'] - 13

        # Prepare Data for Logistic and Linear Regression
        X = df[['Anxiety', 'Stress', 'Depression']]
        y_classification = df['Depression_Increase']
        y_regression = df['Depression_Increase_Magnitude']

        # Train-test split
        X_train, X_test, y_train_class, y_test_class = train_test_split(X, y_classification, test_size=0.2, random_state=42)
        _, _, y_train_reg, y_test_reg = train_test_split(X, y_regression, test_size=0.2, random_state=42)

        # Train Logistic Regression (for classification) and Linear Regression (for magnitude)
        logistic_model = LogisticRegression()
        logistic_model.fit(X_train, y_train_class)

        linear_model = LinearRegression()
        linear_model.fit(X_train, y_train_reg)

        # Save models
        joblib.dump(logistic_model, "dass_logistic_model.pkl")
        joblib.dump(linear_model, "dass_linear_model.pkl")
        print("Models saved successfully.")

        # Evaluate models
        y_pred_class = logistic_model.predict(X_test)
        y_prob = logistic_model.predict_proba(X_test)[:, 1]  # Probability of "Depression_Increase" being 1
        y_pred_reg = linear_model.predict(X_test)

        print("Classification Report:")
        print(classification_report(y_test_class, y_pred_class))
        print(f"Mean Squared Error for Magnitude Prediction: {mean_squared_error(y_test_reg, y_pred_reg):.2f}")

        # Combine Results
        results = pd.DataFrame({
            'Anxiety': X_test['Anxiety'],
            'Stress': X_test['Stress'],
            'Actual_Likelihood': y_test_class,
            'Predicted_Likelihood': y_pred_class,
            'Likelihood (%)': (y_prob * 100).round(2),
            'Actual_Magnitude': y_test_reg,
            'Predicted_Magnitude': y_pred_reg.round(2)
        })

        print("\nResults:")
        print(results.head())

    def load_model(self):
        try:
            if not os.path.exists("dass_logistic_model.pkl") or not os.path.exists("dass_linear_model.pkl"):
                print("Model files not found. Training and saving models...")
                self.train_and_save_model()
            else:
                self.logistic_model = joblib.load("./scripts/dass_logistic_model.pkl")
                self.linear_model = joblib.load("./scripts/dass_linear_model.pkl")
                print("Models loaded successfully.")
        except Exception as e:
            print(f"Error in load_model: {e}")
    

    def compute_scores(self, answers, group_weights=2):
        """Compute the DASS-21 scores for a set of answers, weighted as needed."""
        # Map string answers to numeric values
        answer_map = {
            "Never": 0,
            "Sometimes": 1,
            "Often": 2,
            "Very Often": 3
        }

        # Convert the answers to numeric values
        numeric_answers = [answer_map[answer] for answer in answers]

        return sum(numeric_answers) * group_weights

    def severity_level(self, score, thresholds):
        """Map a score to its severity level based on thresholds."""
        levels = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
        for i, threshold in enumerate(thresholds):
            if score <= threshold:
                return levels[i]
        return levels[-1]

    def predict(self, dAnswers, aAnswers, sAnswers):
        if self.logistic_model is None or self.linear_model is None:
            raise ValueError("Models are not loaded. Call 'load_model' first.")

        # Compute DASS-21 scores
        depression_score = self.compute_scores(dAnswers)
        anxiety_score = self.compute_scores(aAnswers)
        stress_score = self.compute_scores(sAnswers)

        # Map scores to severity levels
        depression_severity = self.severity_level(depression_score, [9, 13, 20, 27])
        anxiety_severity = self.severity_level(anxiety_score, [7, 9, 14, 19])
        stress_severity = self.severity_level(stress_score, [14, 18, 25, 33])

        # Predict likelihood and magnitude of depression increase
        input_data = [[anxiety_score, stress_score, depression_score]]
        likelihood = self.logistic_model.predict_proba(input_data)[0][1]
        magnitude = self.linear_model.predict(input_data)[0]

        return {
            "depression_score": depression_score,
            "depression_severity": depression_severity,
            "anxiety_score": anxiety_score,
            "anxiety_severity": anxiety_severity,
            "stress_score": stress_score,
            "stress_severity": stress_severity,
            "depression_increase_likelihood": likelihood,
            "depression_increase_magnitude": magnitude
        }

#try
#model =DASSModel()
#model.load_model()