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

#rounding values so that it becomes easy for visualization
data['Post_Semester_GPA']=data['Post_Semester_GPA'].round(1)
data['Pre_Semester_GPA']=data['Pre_Semester_GPA'].round(1)
data['Weekly_GenAI_Hours']=data['Weekly_GenAI_Hours'].round(0)
data['Traditional_Study_Hours']=data['Traditional_Study_Hours'].round(0)
data['Skill_Retention_Score']=data['Skill_Retention_Score'].round(0)


#printing all numerical columns to make boxplots to identify outliers
print(data.select_dtypes(include=['float64', 'int64']).columns)
numerical_cols = ['Pre_Semester_GPA', 'Weekly_GenAI_Hours','Difference_in_GPA',
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

# plotting histogram for every numerical column suitable for histogram
histcols=['Pre_Semester_GPA', 'Weekly_GenAI_Hours',
          'Traditional_Study_Hours','Post_Semester_GPA',
       'Skill_Retention_Score', 'Difference_in_GPA']
fig,axes=pt.subplots(2,3,figsize=(12,12))
axes=axes.flatten()
for i,col in enumerate(histcols):
    sb.histplot(data[col],ax=axes[i],kde=True)
    axes[i].set_title(col)
pt.tight_layout()
pt.subplots_adjust(hspace=0.4,wspace=0.4)
pt.show()  


#plotting histogram for Post semester gpa and analysing the capping artifact
sb.histplot(data['Post_Semester_GPA'],kde=True)
pt.title('Post Semester GPA')
pt.show()

""" The values of 4.0 are fairly very high than its neighbors, so looking into it. Checking the counts of each value"""
print(data['Post_Semester_GPA'].value_counts().sort_index(ascending=False).head(15))
""" Post_Semester_GPA shows a capping artifact at 4.0 (4,804 students vs ~20-30 at neighboring values), suggesting the dataset enforces a maximum GPA ceiling rather than reflecting organic distribution."""



#plotting countplots which has ordinal data
fig,axes=pt.subplots(3,3,figsize=(12,12))
axes=axes.flatten()
order1=['Freshman','Sophomore','Junior','Senior','Graduate']    
sb.countplot(x=data['Year_of_Study'], data=data, order=order1, ax=axes[0])
axes[0].set_title('Year of Study')
axes[0].set_xlabel('')   

order2=['Beginner','Intermediate','Advanced']
sb.countplot(x=data['Prompt_Engineering_Skill'], data=data, order=order2, ax=axes[1])
axes[1].set_title('Prompt Engineering Skill')
axes[1].set_xlabel('')

order3=[1,2,3,4,5]
sb.countplot(x=data['Tool_Diversity'], data=data, order=order3, ax=axes[2])
axes[2].set_title('Tool Diversity')
axes[2].set_xlabel('')

order4=[1,2,3,4,5,6,7,8,9,10]
sb.countplot(x=data['Perceived_AI_Dependency'],data=data,order=order4,ax=axes[3])
axes[3].set_title('Perceived AI Dependency')
axes[3].set_xlabel('')

order5=['Actively_Encouraged','Allowed_With_Citation','Strict_Ban']
sb.countplot(x=data['Institutional_Policy'],data=data,order=order5, ax=axes[4])
axes[4].set_title('Institutional Policy')
axes[4].tick_params(axis='x', rotation=15)
axes[4].set_xlabel('')

order6=[1,2,3,4,5,6,7,8,9,10]
sb.countplot(x=data['Anxiety_Level_During_Exams'],data=data,order=order6, ax=axes[5])
axes[5].set_title('Anxiety Level During Exams')
axes[5].set_xlabel('')

order7 = ['Low', 'Medium', 'High']
sb.countplot(x=data['Burnout_Risk_Level'], data=data, order=order7, ax=axes[6])
axes[6].set_title('Burnout Risk Level')
axes[6].set_xlabel('')

pt.subplots_adjust(hspace=0.4,wspace=0.4)
axes[7].axis('off')
axes[8].axis('off')
pt.tight_layout()
pt.show()

#plotting countplots for categorical data

fig,axes=pt.subplots(1,3,figsize=(13,5))
sb.countplot(y=data['Primary_Use_Case'],data=data, ax=axes[0])
axes[0].set_title('Primary Use Case')
axes[0].set_ylabel('')

sb.countplot(y=data['Major_Category'],data=data,ax=axes[1])
axes[1].set_title('Major Category')
axes[1].set_ylabel('')

sb.countplot(x=data['Paid_Subscription'],data=data, ax=axes[2])
axes[2].set_title('Paid Subscription')
axes[2].set_ylabel('')

pt.subplots_adjust(hspace=0.4,wspace=0.4,left=0.2)
pt.show()