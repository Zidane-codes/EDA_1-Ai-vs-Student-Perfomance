#importing the necessary libraries
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as pt

#reading the csv data file and converting into pandas dataframe
data = pd.read_csv("Z:/Projects/EDA_1/ai_student_impact_dataset.csv")
print(data.head(10))                                                         #printing first 10 records to check the data frame

#check for null values
nullv = data.isnull().sum()
print(nullv)

#check for duplicate values
datad=data.duplicated().sum()
print(datad)

#describing and understanding the structure of the data with its datatypes
print(data.info())                                                           #checking columns
print(data.describe())    
print(data.dtypes)

# Data transformation: New column Difference in GPA added for better analysis
data['Difference_in_GPA'] = data['Post_Semester_GPA'] - data['Pre_Semester_GPA']
print(data['Difference_in_GPA'])


#printing all numerical columns to make boxplots to identify outliers
print(data.select_dtypes(include=['float64', 'int64']).columns)
numerical_cols = ['Student_ID', 'Pre_Semester_GPA', 'Weekly_GenAI_Hours',
                  'Tool_Diversity', 'Traditional_Study_Hours', 'Perceived_AI_Dependency',
                  'Anxiety_Level_During_Exams', 'Post_Semester_GPA', 'Skill_Retention_Score']

#plotting the boxplot
fig, axes=pt.subplots(3,3,figsize=(15,15))
axes=axes.flatten() 
for i,col in enumerate(numerical_cols):
    data.boxplot(column=[col],ax=axes[i])
    axes[i].set_title(col)
    axes[i].set_xticklabels([])

pt.show()


#weekly genai has value of 40 hours/week which seems unrealistic so will remove the edgy outliers
data.boxplot(column=['Weekly_GenAI_Hours'])
pt.show()
#there are outliers past Q3 so will remove them
Q1 = data['Weekly_GenAI_Hours'].quantile(0.25)
Q3 = data['Weekly_GenAI_Hours'].quantile(0.75)
IQR = Q3 - Q1
upper_limit = Q3 + 2 * IQR
cleaned_genai_hours= data[data['Weekly_GenAI_Hours'] <= upper_limit]


fig,axes=pt.subplots(1,2,figsize=(10,5))
data.boxplot(column=['Weekly_GenAI_Hours'], ax=axes[0])
axes[0].set_title('Before')

cleaned_genai_hours.boxplot(column=['Weekly_GenAI_Hours'], ax=axes[1])
axes[1].set_title('After')
pt.show()

