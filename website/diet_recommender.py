from async_generator import async_generator
import joblib
from sqlalchemy import true
import pandas as pd
import random

class Diet_Recommender:
    def __init__(self, user_database, target, user_activity_level, motivation):
        self.gender = user_database.user_gender
        self.age = user_database.user_age
        self.height = user_database.user_height
        self.weight = user_database.user_weight
        self.exercise = user_activity_level

        if self.exercise == 'Sedentary':
            self.lifestyle = '1. Sedentary or light activity (e.g. - Office worker getting little or no exercise)'
        elif self.exercise == 'Lightly active' or 'Moderately active':
            self.lifestyle = '2. Active or moderately active (Construction worker or person running one hour daily)'
        elif self.exercise == 'Vigorously active':
            self.lifestyle = '3. Vigorously active (Agricultural worker (non mechanized) or person swimming two hours daily)'
                
        # this value in unknown
        self.daily_calories_intake = 2100
        self.target = target

        if motivation == 'scale-1':
            self.motivation = random.randint(60, 79)
        elif motivation == 'scale-2':
            self.motivation = random.randint(80, 85)
        if motivation == 'scale-3':
            self.motivation = random.randint(86, 90)
        if motivation == 'scale-4':
            self.motivation = random.randint(91, 95)
        
        self.bmi = user_database.user_bmi
        self.bmr = user_database.user_bmr
        
        if self.gender == 'Male':
            if self.age <= 20:
                self.type = 'Boy'
                self.bfp = (1.51*self.bmi) - (0.7*self.age) - (3.6*1) + 1.4
            else:
                self.type = 'Adult Male'
                self.bfp = (1.39*self.bmi) - (0.16*self.age) - (10.34*1) - 9
        
        elif self.gender == 'Female':
            if self.age <= 20:
                self.type = 'Girl'
                self.bfp = (1.51*self.bmi) - (0.7*self.age) - (3.6*0) + 1.4
            else:
                self.type = 'Adult Female'
                self.bfp = (1.39*self.bmi) - (0.16*self.age) - (10.34*0) - 9
        
        if self.bmi < 18:
            self.body_type = 'Underweight'
        elif self.bmi >= 18.5 and self.bmi <= 24.9:
            self.body_type = 'Normal'
        elif self.bmi >= 25 and self.bmi <= 29.9:
            self.body_type = 'Overweight'
        elif self.bmi >= 30:
            self.body_type = 'Obese'

        # Based on BMR and Exercise
        if self.exercise == 'Sedentary':
            self.daily_calories_needed = round(self.bmr * 1.2)
        elif self.exercise == 'Lightly active': 
            self.daily_calories_needed = round(self.bmr * 1.375) 
        elif self.exercise == 'Moderately active':
            self.daily_calories_needed = round(self.bmr * 1.465)
        elif self.exercise == 'Vigorously active':
            self.daily_calories_needed = round(self.bmr * 1.725)
        
        self.tdee = 2200
        self.calorie_diff = round((self.daily_calories_intake - self.tdee)/self.tdee, 6)

    def print_all(self):
        print(self.exercise)
        print(self.lifestyle)
        print(self.type)
        print(self.bfp)
        print(self.body_type)
        print(self.daily_calories_needed)
        print(self.calorie_diff)

    def map_variables(self):
        self.user_Dataframe = [[self.gender, self.age, self.height, self.weight, 
                                self.lifestyle, self.exercise, self.daily_calories_intake,
                                self.target, self.motivation, self.bmi,
                                self.bmr, self.type, self.bfp, self.body_type,
                                self.daily_calories_needed, self.tdee, self.calorie_diff]]

        self.df = pd.DataFrame(self.user_Dataframe)
        self.df.columns = [  'Gender', 'Age', 'Height(cm)', 'Weight(kg)', 'Lifestyle',
                        'Exercise', 'Daily Calories Intake', 'Target',
                        'How motivated are you for being healthy\n(in %)',
                        'Body Mass Index (BMI)', 'Basal Metabolic Rate (BMR)', 'Type',
                        'Body Fat Percentage (BFP)', 'Body Type',
                        'Daily Calorie Need (Based on BMR and Exercise)\n(in Calorie)',
                        'Total Daily Energy Expenditure (TDEE) (Based on BMR and Lifestyle)\n(in Calorie)',
                        'Calorie Difference (Daily Calorie Intake - TDEE)']
        
        # mapping categorical to numeric values
        self.df['Gender']=self.df['Gender'].map({"Male":0,"Female":1})
        self.df['Body Type']=self.df['Body Type'].map({"Underweight":0,"Normal":1,"Overweight":2,"Obese":3})
        self.df['Type']=self.df['Type'].map({"Boy":0,"Girl":1,"Adult Male":2,"Adult Female":3})
        self.df['Target']=self.df['Target'].map({"Loose Weight":0,"Maintain Weight":1,"Gain Muscle":2})
        self.df['Lifestyle']=self.df['Lifestyle'].map({"1. Sedentary or light activity (e.g. - Office worker getting little or no exercise)":0,"2. Active or moderately active (Construction worker or person running one hour daily)":1,"3. Vigorously active (Agricultural worker (non mechanized) or person swimming two hours daily)":2})
        self.df['Exercise']=self.df['Exercise'].map({"Sedentary":0,"Lightly active":1,"Moderately active":2,"Vigorously active":3})
        #df.to_csv('user_data.csv')
        #print(df)
        #print(df.shape)

    def predict(self):
 
        self.model = joblib.load('website/diet_recommendation.pkl')
        self.diet_prediction = self.model.predict(self.df)

        return(self.diet_prediction[0])
