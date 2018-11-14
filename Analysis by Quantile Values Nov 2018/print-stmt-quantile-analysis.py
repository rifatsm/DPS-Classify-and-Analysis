###################################
# print-stmt-quantile-analysis.py #
###################################

# This Python script is to classify the print statements to DPS and Non-DPS (Step 1-4)
# This Python script further analyzes the print statements based on the quantile scores (Step 5)

import os
import pandas as pd

# Reading the CSV file containing all the print statements
print "Initiating `print-stmt-quantile-analysis` script:"
# print_stmt = pd.read_csv("/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/print-stmt all versions/Oct 22, 2018/print-stmts.csv")
print_stmt_filename = ""

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
file_directory_project_1 = ""

# Project 2 file directory
file_directory_project_2 = ""

# Project 3 file directory
#file_directory_project_3 = ""

# Project 4 file directory
file_directory_project_4 = ""

# List of empty and trivial print statements 
trivial_print_stmt = []

'''
Description: Storing values in the global variables
Params: None
Return: None
'''
def storing_values_in_global_vars():

	global print_stmt_filename, file_directory_project_1, file_directory_project_2, file_directory_project_4

	# CSV file with all the print statements
	print_stmt_filename = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/print-stmt all versions/Nov 09, 2018/print-stmts.csv"

	# Project 1 file directory
	file_directory_project_1 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_1.txt"

	# Project 2 file directory
	file_directory_project_2 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_2.txt"

	# Project 3 file directory (Empty)
	#file_directory_project_3 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_3.txt"

	# Project 4 file directory
	file_directory_project_4 = "/Users/Ri/ToyRepo/CS3114F16_Oracle_Sample_Outputs_simplified/output_samples_Project_4.txt"
	pass

'''
Description: Storing trivial print statements values 
Params: None
Return: None
'''
def storing_trivial_print_stmt():
	global trivial_print_stmt
	# List of empty and trivial print statements 
	trivial_print_stmt = ['System.out.println()', '("" -> "")', 'System.out.println("""")', '-> "")', '(""\n"");', '("");', 'System.out.println("" "")', 'System.out.print()', '(""->"");', '(""\n\n"")', '(""\n \n"")', 'System.out.print);', 'System.out.println("" "");']
	pass


'''
Description: Function to read all the data in the CSV file 
Params: filename = name of the CSV file with path directory
Return: Dataframe
'''
def read_all_data(filename):
	return pd.read_csv(filename)


'''
Description: Reading the specific required output statements for a particular project 
Params: project_spec_list = the project specific global list containing required output statements for that particular project 
		file_directory = the TXT file containing all the required output statements for that particular project 
Return: None
'''
def read_specs(project_spec_list, file_directory):
	with open(file_directory) as file_read:
		for line in file_read:
			line = line.replace('\r\n','') # Getting rid of carriage return and newline 
			line = line.replace('\n', '') # Getting rid of only newline 
			project_spec_list.append(line)
	# print "Project specs: "
	# print project_spec_list
	pass

'''
Description: Classifies print statements to DPS or Non-DPS based on the criteria mentioned inside the function
Params: print_stmt_list = List of all the print statements
		project_no = Project no 
Return: None
'''
def classify_dps(print_stmt_list, project_no):

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

	print "Iterating over rows of `print_stmt_list`...",
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
	print "(Done)"
	# Converting List into Series in order to add as a new column to the existing dataframe 
	dps_series = pd.Series(dps_list)
	# Adding the values of the Series to the new column 
	print_stmt_list['DPS'] = dps_series.values

	print "Outputting to CSV file...",
	output_directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_Python_script/Projectwise all PS/"
	print_stmt_list.to_csv(output_directory +project_no+ "_print_stmt_list.csv", index=False)
	print "(Done)"
	pass

'''
Description: Counts the DPS for each of the projects
Params: print_stmt_filename = file containing all the print statements for a particular project
		project_no = Project No
Return: None
'''

def counting_DPS(print_stmt_filename, project_no):
	print "Reading file: " + print_stmt_filename,
	print_stmt_list = read_all_data(print_stmt_filename)
	print " (Done)"
	unique_project_list = print_stmt_list.userId.unique()

	total_list = []
	dps_list = []
	n_dps_list = []
	count = 0
	print "Counting Total PS, DPS, and Non-DPS...",
	for project_userId in unique_project_list:
		# Gettting the number of rows for a specific userId
		_temp_total = print_stmt_list.loc[print_stmt_list['userId'] == project_userId].userId.count()
		total_list.append(_temp_total)
		# Getting the number of DPS for a specific userId
		_temp_dps = print_stmt_list.loc[(print_stmt_list['userId'] == project_userId) & (print_stmt_list['DPS'] == 1)].userId.count()
		dps_list.append(_temp_dps)
		n_dps_list.append(_temp_total - _temp_dps)
	print "(Done)"

	# Converting list to dataframe 
	print "Merging all in one dataframe...",
	print_stmt_df = pd.DataFrame()
	print_stmt_df['userId'] = unique_project_list
	print_stmt_df['Total PS'] = total_list
	print_stmt_df['DPS count'] = dps_list
	print_stmt_df['Non-DPS count'] = n_dps_list
	print "(Done)"

	# Renaming column name to 'userId'
	# print_stmt_df = print_stmt_df.rename(index=str, columns={"0": "userId"})
	# print print_stmt_df

	# Output the dataframe to a CSV file 
	print "Outputting to CSV file...",
	output_directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_Python_script/Project PS Counted/"
	print_stmt_df.to_csv(output_directory +project_no+ "_ps_counted.csv", index=False)
	print "(Done)"

	pass

'''
Description: Merges project score to the project 
Params: score_filename = File containing scores for all the projects
		print_stmt_filename = File containing all the print statements for a particular project
		project_no = Project No
Return: None
'''
def merging_scores(score_filename, print_stmt_filename, project_no):
	# Reading files
	print "Reading file: " + score_filename,
	score_list = read_all_data(score_filename)
	print " (Done)"
	print "Reading file: " + print_stmt_filename,
	ps_counted_list = read_all_data(print_stmt_filename)
	print " (Done)"

	# Filtering scores
	score_list = score_list.loc[score_list['assignment'] == project_no]
	score_df = pd.DataFrame()
	score_df['userId'] = score_list['userName']
	score_df['Score'] = score_list['score.correctness']
	# print "score_df"
	# print score_df

	# Merging score w/ counted ps
	score_merged = pd.merge(ps_counted_list, score_df, how='left', on='userId')
	# print "score_merged"
	# print score_merged

	# Output the dataframe to a CSV file 
	print "Outputting the merged df to CSV file...",
	output_directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_Python_script/PS Counted + Score Merged/"
	score_merged.to_csv(output_directory +project_no+ "_ps_count_n_score_merged.csv", index=False)
	print "(Done)"
	pass

'''
Description: Dividing score merged projects by quantile scores
Params: merged_filename = File containing ps count and score merged projects
		quantile_directory = Directory containing projectwise quantile scores
		project_no = Project No
Return: None
'''
def diving_projects_by_quantile_scores(merged_filename, quantile_directory, project_no):
	# Reading the files
	print "Reading file: " + merged_filename,
	score_data = read_all_data(merged_filename)
	print " (Done)"

	# Selecting Project directory
	if(project_no == "Project 1"):
		quantile_directory = quantile_directory + project_no + "/"
	if(project_no == "Project 2"):
		quantile_directory = quantile_directory + project_no + "/"
	if(project_no == "Project 3"):
		quantile_directory = quantile_directory + project_no + "/"
	if(project_no == "Project 4"):
		quantile_directory = quantile_directory + project_no + "/"

	quantile_files = os.listdir(quantile_directory)

	# print "quantile_files"
	# print quantile_files

	# Listing projects by quantile scores
	quantile_score_list = [[],[],[],[]]
	for file in quantile_files:
		if "q_0_to_25" in file:
			quantile_score_list[0] = read_all_data(quantile_directory+file).userName.unique()
		if "q_25_to_50" in file:
			quantile_score_list[1] = read_all_data(quantile_directory+file).userName.unique()
		if "q_50_to_75" in file:
			quantile_score_list[2] = read_all_data(quantile_directory+file).userName.unique()
		if "q_75_to_100" in file:
			quantile_score_list[3] = read_all_data(quantile_directory+file).userName.unique()


	# Printing the list 
	# for _list in quantile_score_list:
	# 	print "_list " + str(len(_list))
	# 	print _list

	# Creating dataframe for each of the quantile scores
	quantile_1 = pd.DataFrame()
	quantile_2 = pd.DataFrame()
	quantile_3 = pd.DataFrame()
	quantile_4 = pd.DataFrame()

	quantile_1['userId'] = quantile_score_list[0]
	quantile_1['Quantile'] = "1"

	quantile_2['userId'] = quantile_score_list[1]
	quantile_2['Quantile'] = "2"

	quantile_3['userId'] = quantile_score_list[2]
	quantile_3['Quantile'] = "3"

	quantile_4['userId'] = quantile_score_list[3]
	quantile_4['Quantile'] = "4"

	# Join 4 dataframes into one dataframe 
	dataframes = [quantile_1, quantile_2, quantile_3, quantile_4]
	quantile_df = pd.concat(dataframes)

	# Merging the quantile type to the ps + score data
	score_data = pd.merge(score_data, quantile_df, how='left', on='userId')

	# Output the dataframe to a CSV file 
	print "Outputting the merged df to CSV file...",
	output_directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_Python_script/PS Count + Score + Quantile Merged/"
	score_data.to_csv(output_directory +project_no+ "_ps_count_n_score_n_quantile_merged.csv", index=False)
	print "(Done)"

	pass


##############
# Debug Mode #
##############
'''
Description: For debugging purposes, please set the debug_mode ON. 
			For running the actual steps, please reset the debug_mode to 0 (zero). 
'''
debug_mode = 0

##################
# Step Selection #
##################
'''
Description: The below are the actual steps to be executed  
			 Set all the steps that you wish to execute
'''
# Declaring and initializing to 0 (zero)
step_1 = 0
step_2 = 0
step_3 = 0
step_4 = 0
step_5 = 0
step_6 = 0
step_7 = 0

# Setting values to the steps we want to execute
# step_1 = 1
# step_2 = 1
# step_3 = 1
# step_4 = 1
# step_5 = 1
# step_6 = 1
step_7 = 1

#########
# Steps #
#########
if(debug_mode == 0):

	if(step_1 == 1):
		# Step 1
		'''
		Description: Setting up the environment
		'''
		print "##########"
		print "# Step 1 #"
		print "##########"
		# Populating global values
		print "Populating global values ",
		storing_values_in_global_vars()
		storing_trivial_print_stmt()
		print "(Done)"

	if(step_2 == 1):
		# Step 2
		'''
		Description: Getitng all the print statement (for all the projects)
		'''
		print "##########"
		print "# Step 2 #"
		print "##########"
		# Reading all the print statements from the CSV file 
		print "Reading all the print statements from the CSV file ",
		all_print_stmts = read_all_data(print_stmt_filename)
		print "(Done)"

	if(step_3 == 1):
		# Step 3
		'''
		Description: Preparing the required output specifications
		'''
		print "##########"
		print "# Step 3 #"
		print "##########"
		# Reading required output specifications for each of the 4 projects 
		# Except Project 3, because we do not have any specific required output for Project 3. 
		print "Gathering project specs for Project 1 ",
		read_specs(project_spec_1, file_directory_project_1)
		print "(Done)"
		print "Gathering project specs for Project 2 ",
		read_specs(project_spec_2, file_directory_project_2)
		print "(Done)"
		# print "Gathering project specs for Project 3"
		# read_specs(project_spec_3, file_directory_project_3)
		print "Gathering project specs for Project 4 ",
		read_specs(project_spec_4, file_directory_project_4)
		print "(Done)"

	if(step_4 == 1):
		# Step 4
		'''
		Description: Classifying all the print statements
		'''
		print "##########"
		print "# Step 4 #"
		print "##########"
		# Classify print statements into DPS and Non-DPS
		print "Classifying Project 1"
		classify_dps(all_print_stmts, "Project 1")
		print "Classifying Project 2"
		classify_dps(all_print_stmts, "Project 2")
		print "Classifying Project 3"
		classify_dps(all_print_stmts, "Project 3")
		print "Classifying Project 4"
		classify_dps(all_print_stmts, "Project 4")

	if(step_5 == 1):
		# Step 5 
		'''
		Description: Getting Total PS count, DPS count, and Non-DPS count for each projects
		'''
		print "##########"
		print "# Step 5 #"
		print "##########"
		# Getting the files for each of the 4 projects
		directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_Python_script/Projectwise all PS/"
		project_1_filename = directory + "Project 1_print_stmt_list.csv"
		project_2_filename = directory + "Project 2_print_stmt_list.csv"
		project_3_filename = directory + "Project 3_print_stmt_list.csv"
		project_4_filename = directory + "Project 4_print_stmt_list.csv"
		
		# Running the counting functions
		print "Running counting_DPS for Project 1"
		counting_DPS(project_1_filename, "Project 1")
		print "Running counting_DPS for Project 2"
		counting_DPS(project_2_filename, "Project 2")
		print "Running counting_DPS for Project 3"
		counting_DPS(project_3_filename, "Project 3")
		print "Running counting_DPS for Project 4"
		counting_DPS(project_4_filename, "Project 4")

	if(step_6 == 1):
		# Step 6
		'''
		Description: Merging project scores
		'''
		print "##########"
		print "# Step 6 #"
		print "##########"

		# Reading all the PS counted CSV files
		directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_Python_script/Project PS Counted/"
		project_1_filename = directory + "Project 1_ps_counted.csv"
		project_2_filename = directory + "Project 2_ps_counted.csv"
		project_3_filename = directory + "Project 3_ps_counted.csv"
		project_4_filename = directory + "Project 4_ps_counted.csv"

		# Reading file containing the scores from all the projects
		directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/"
		score_filename = directory + "web-cat-all_output_submission_data.csv"

		# Calling the merging functions
		print "Running merging_scores for Project 1"
		merging_scores(score_filename, project_1_filename, "Project 1")
		print "Running merging_scores for Project 2"
		merging_scores(score_filename, project_1_filename, "Project 2")
		print "Running merging_scores for Project 3"
		merging_scores(score_filename, project_1_filename, "Project 3")
		print "Running merging_scores for Project 4"
		merging_scores(score_filename, project_1_filename, "Project 4")

	if(step_7 == 1):
		# Step 7
		'''
		Description: Dividing scores into Quantile scores
		'''
		print "##########"
		print "# Step 7 #"
		print "##########"

		# Reading all the PS counted + score merged CSV files
		directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_Python_script/PS Counted + Score Merged/"
		project_1_filename = directory + "Project 1_ps_count_n_score_merged.csv"
		project_2_filename = directory + "Project 2_ps_count_n_score_merged.csv"
		project_3_filename = directory + "Project 3_ps_count_n_score_merged.csv"
		project_4_filename = directory + "Project 4_ps_count_n_score_merged.csv"

		# Directory for projectwise quantile scores
		quantile_directory = "/Dr. Cliff Shaffer's Lab/DPS Classify and Analysis Oct, 2018/Analysis by Quantile Values Nov 2018/From_R_script/QuantileScoreWise/"

		# Calling function to divide merged projects
		print "Running `diving_projects_by_quantile_scores` for Project 1"
		diving_projects_by_quantile_scores(project_1_filename, quantile_directory, "Project 1")
		print "Running `diving_projects_by_quantile_scores` for Project 2"
		diving_projects_by_quantile_scores(project_1_filename, quantile_directory, "Project 2")
		print "Running `diving_projects_by_quantile_scores` for Project 3"
		diving_projects_by_quantile_scores(project_1_filename, quantile_directory, "Project 3")
		print "Running `diving_projects_by_quantile_scores` for Project 4"
		diving_projects_by_quantile_scores(project_1_filename, quantile_directory, "Project 4")







elif(debug_mode == 1):
	# Inside Debug Mode 
	print "##############"
	print "# Debug Mode #"
	print "##############"
	pass
else:
	print "Invalid mode!"

# Closing the Python Script	
print "Closing the script. Bye!"
