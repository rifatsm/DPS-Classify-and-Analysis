##############################
# print-stmt-dps-classify.py #
##############################

# This Python script is to classify the print statement to DPS and Non-DPS

import pandas as pd

# Reading the CSV file containing all the print statements
print "Reading print_stmt..."
print_stmt = pd.read_csv("/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/print-stmt all versions/Oct 22, 2018/print-stmt.csv")

# Dataframe for selected projects (score higher than the threshold value)
selected_projects = pd.DataFrame()

# Dataframe for ZERO projects (score equal to ZERO)
zero_projects = pd.DataFrame()

# Dataframe for all the print statements in the selected projects with high score
print_stmt_high_score = pd.DataFrame()

# Dataframe for all the print statements in the selected projects with low score
print_stmt_low_score = pd.DataFrame()

# List of required phrases of Project 1
project_spec_1 = []

# List of required phrases of Project 2
project_spec_2 = []

# List of required phrases of Project 3 (empty)
project_spec_3 = []

# List of required phrases of Project 4
project_spec_4 = []

# Project 1 file directory
file_directory_project_1 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_1.txt"

# Project 2 file directory
file_directory_project_2 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_2.txt"

# Project 3 file directory
#file_directory_project_3 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_3.txt"

# Project 4 file directory
file_directory_project_4 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_4.txt"

# List of empty and trivial print statements 
trivial_print_stmt = ['System.out.println()', '("" -> "")', 'System.out.println("""")', '-> "")', '(""\n"");', '("");', 'System.out.println("" "")', 'System.out.print()', '(""->"");', '(""\n\n"")', '(""\n \n"")', 'System.out.print);', 'System.out.println("" "");']



def concatenate_func():

	# Getting all the projects with score higher than threshold score 
	# Selecting only columns `userName`, `assignment`, and `score`
	# Getting the `userName` and the `assignment` concatenated and then added to a dataframe 

	# Scores below the threshold score
	# print consolidated[consolidated.score < 0.50] # 68 rows

	# Reading the CSV file containing all the project with project score
	# We read it to put a threshold score to all the projects and select the ones with higher score than the threshold score 
	print "Reading consolidated.csv"
	consolidated = pd.read_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/consolidated.csv")

	threshold_score = 0.50
	column_list = ['userName', 'assignment', 'score']
	print "Getting all the projects with score higher than threshold score..."
	consolidated_modified = consolidated[consolidated.score >= threshold_score].loc[:, consolidated.columns.isin(column_list)] # 367 rows
	print "For consolidated_modified, getting the `userName` and the `assignment` concatenated and then added to a dataframe..."
	selected_projects['concatenated'] = consolidated_modified[['userName', 'assignment']].apply(lambda x: '__'.join(x), axis=1)

	print "Getting all the projects with ZERO score"
	consolidated_zero = consolidated[consolidated.score == 0].loc[:, consolidated.columns.isin(column_list)] # 50 rows
	print "For consolidated_zero, getting the `userName` and the `assignment` concatenated and then added to a dataframe..."
	zero_projects['concatenated'] = consolidated_zero[['userName', 'assignment']].apply(lambda x: '__'.join(x), axis=1)

	print "Outputting selected_projects.csv"
	selected_projects.to_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/selected_projects.csv", index=False)
	
	print "Outputting zero_projects.csv"
	zero_projects.to_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/zero_projects.csv", index=False)

	print "Making a copy of print_stmt"
	print_stmt_modified = print_stmt
	print "For print_stmt, getting the `userName` and the `assignment` concatenated..."
	print_stmt_modified['concatenated'] = print_stmt[['userId', 'CASSIGNMENTNAME']].apply(lambda x: '__'.join(x), axis=1)

	print "Discarding the ZERO projects from the print_stmt_modified"
	print_stmt_modified = print_stmt_modified.loc[~print_stmt_modified['concatenated'].isin(zero_projects['concatenated'].tolist())]

	print "Discarding the deletion instances of the print statements in print_stmt_modified"
	print_stmt_modified = print_stmt_modified.loc[print_stmt_modified['Subsubtype'] != 'Deletion']

	print "Outputting print_stmt_modified.csv"
	print_stmt_modified.to_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/print_stmt_modified.csv", index=False)

	print "Merging (Inner Join) two dataframes... Getting print statements w/ high score"
	print_stmt_high_score = pd.merge(print_stmt_modified, selected_projects[['concatenated']], how='inner', on='concatenated')

	print "Getting print statements w/ low score"
	print_stmt_low_score = print_stmt_modified.loc[~print_stmt_modified['concatenated'].isin(selected_projects['concatenated'].tolist())]

	# TODO discard the column `concatenated` from `print_stmt_modified` and `print_stmt_high_score`

	print "Outing print_stmt_high_score.csv"
	print_stmt_high_score.to_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/print_stmt_high_score.csv", index=False)

	print "Outing print_stmt_low_score.csv"
	print_stmt_low_score.to_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/print_stmt_low_score.csv", index=False)


	# Here, the `print_stmt_modifeid` dataframe contains 80284 rows. 
	# On the contrary, the `print_stmt_high_score` dataframe contains 45337 rows. 
	pass

def read_specs(project_spec_list, file_directory):
	with open(file_directory) as file_read:
		for line in file_read:
			line = line.replace('\r\n','') # Getting rid of carriage return and newline 
			line = line.replace('\n', '') # Getting rid of only newline 
			project_spec_list.append(line)
	# print "Project specs: "
	# print project_spec_list
	pass

def classify_dps(print_stmt_list, project_no, high_or_low):

	## Classifying DPS based the following criteria:
	# A DPS cannot be an empty statement (such as, 'System.out.println()')
	# A DPS cannot be a trivial statement (such as, 'System.out.print("\n")')
	# A DPS cannot be a `Final` statement (print statements that appear in the final submission)
	# A DPS cannont contain any element of the project specifications (The required print statements for Web-CAT test cases)
	# If none of the above criteria is satisfied then we can classify the statement as a potential DPS

	# First take the sample set of the specified project by pruning the total dataset 
	print_stmt_list = print_stmt_list.loc[print_stmt_list['CASSIGNMENTNAME'] == project_no]

	# Selecting project spec 
	if project_no == 'Project 1':
		project_spec = project_spec_1
	elif project_no == 'Project 2':
		project_spec = project_spec_2
	elif project_no == 'Project 3':
		project_spec = project_spec_3
	elif project_no == 'Project 4':
		project_spec = project_spec_4

	# List of DPS values
	dps_list = []

	print "Iterating over rows of `print_stmt_list`..."
	# Iterate over rows 
	for index, row in print_stmt_list.iterrows():
		dps_value = 1

		# Checking for Trivial print statements
		if any(phrase in row['PrintStatements'] for phrase in trivial_print_stmt):
			dps_value = 0
			# print "Trivial: " + row['PrintStatements'] 
		# Checking for `Final` statements
		if row['Subtype'] == 'Final':
			dps_value = 0
		# Checking for project specs 
		if any(spec in row['PrintStatements'] for spec in project_spec):
			dps_value = 0

		dps_list.append(dps_value)

	# Converting List into Series in order to add as a new column to the existing dataframe 
	dps_series = pd.Series(dps_list)
	# Adding the values of the Series to the new column 
	print_stmt_list['DPS'] = dps_series.values

	print "Outputting to CSV file..."
	print_stmt_list.to_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/" +project_no+ "_print_stmt_list_" + high_or_low + ".csv", index=False)
	pass

# Step 1

# # Running functions
# concatenate_func()

# Step 2 (Run the following together)

# Getting all the specs
print "Gathering project specs for Project 1"
read_specs(project_spec_1, file_directory_project_1)
print "Gathering project specs for Project 2"
read_specs(project_spec_2, file_directory_project_2)
# print "Gathering project specs for Project 3"
# read_specs(project_spec_3, file_directory_project_3)
print "Gathering project specs for Project 4"
read_specs(project_spec_4, file_directory_project_4)

# Reading the CSV generated by concatenate_func(), so that we do not have to run the func more than once
print "Classifying print statements w/ high score"
print_stmt_high_score = pd.read_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/print_stmt_high_score.csv")
print_stmt_high_score = print_stmt_high_score.drop(columns=['concatenated'])
# Classifying print statements with high score
classify_dps(print_stmt_high_score, "Project 1", "high")
classify_dps(print_stmt_high_score, "Project 2", "high")
classify_dps(print_stmt_high_score, "Project 3", "high")
classify_dps(print_stmt_high_score, "Project 4", "high")

# Reading the CSV generated by concatenate_func(), so that we do not have to run the func more than once
print "Classifying print statements w/ low score"
print_stmt_low_score = pd.read_csv("/Summer 2018/Dr. Cliff Shaffer's Lab/DSP vs Launch Times Analysis/Selecting_DPS_w_threshold/print_stmt_low_score.csv")
print_stmt_low_score = print_stmt_low_score.drop(columns=['concatenated'])
# Classifying print statements with low score
classify_dps(print_stmt_low_score, "Project 1", "low")
classify_dps(print_stmt_low_score, "Project 2", "low")
classify_dps(print_stmt_low_score, "Project 3", "low")
classify_dps(print_stmt_low_score, "Project 4", "low") 
