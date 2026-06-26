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

#plotting histogram for Pre semester gpa
sb.histplot(data['Pre_Semester_GPA'],kde=True)
pt.title('Pre Semester GPA')
pt.show()

#plotting histogram for Post semester gpa
sb.histplot(data['Post_Semester_GPA'],kde=True)
pt.title('Post Semester GPA')
pt.show()

""" The values of 4.0 are fairly very high than its neighbors, so looking into it. Checking the counts of each value"""
print(data['Post_Semester_GPA'].value_counts().sort_index(ascending=False).head(15))
""" Post_Semester_GPA shows a capping artifact at 4.0 (4,804 students vs ~20-30 at neighboring values), suggesting the dataset enforces a maximum GPA ceiling rather than reflecting organic distribution."""
""" This was because of decimal values of GPA and for values such as 3.999 they get skimmed to 4.0 """
""" To prevent this, I cut off the decimals to just one decimal, so that the values are relevant and also work properly with graphs"""
data['Post_Semester_GPA']=data['Post_Semester_GPA'].round(1)
data['Pre_Semester_GPA']=data['Pre_Semester_GPA'].round(1)
data['Difference_in_GPA']=data['Difference_in_GPA'].round(1)

col=['Pre_Semester_GPA','Post_Semester_GPA','Difference_in_GPA']
fig,axes=pt.subplots(2,2,figsize=(12,12))
axes=axes.flatten()
for i,col in (col):
    pt.hist(columns=data[col],ax=axes[i])
    axes[i].set_title(col)
    axes[i].set_xticklabels([])

pt.show()
