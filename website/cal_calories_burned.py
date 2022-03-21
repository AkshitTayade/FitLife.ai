# MET values referred from - https://golf.procon.org/met-values-for-800-activities/
# https://wiisports.fandom.com/wiki/Metabolic_Equivalent_Task_(MET)
# healthy weight loss rate is 0.5 - 1 kg per week.

class CalorieBurned():
    def __init__(self, total_seconds, exercise_name, user_weight):
        self.MET_value = {  "jumping jack": 8,
                            "adbominal crunches": 2.8,
                            "knee pushup": 3.8,
                            "side arm raises": 3,
                            "squat": 5,
                            "backward lunges": 3.8,
                            "cobra stretch": 2.3  }

        self.total_time_in_min = total_seconds/60
        self.exercise_name = exercise_name
        self.user_weight = user_weight

    def getMET(self):
        self.met = self.MET_value[self.exercise_name]
        return(self.met)

    def calculate(self):
        
        MET = self.getMET()
        calories = (self.total_time_in_min * MET * 3.5 * self.user_weight)  / 200
        weight_loss = calories/7700
        
        # print(f"Energy burned: {calories} cal")
        # print(weight_loss, round(weight_loss,5))
        
        return(round(calories, 4), round(weight_loss,5))
