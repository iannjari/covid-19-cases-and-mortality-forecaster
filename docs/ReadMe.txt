NAME: IAN MOSES NJARI

REG NO.: J17/0803/2017

SUPERVISOR: MR. JOSEPH MURIUKI MWANGI, M.Sc.

PROJECT TITLE: COVID-19 CASELOAD AND MORTALITY ANALYSIS AND PREDICTION WITH MACHINE LEARNING

ACADEMIC YEAR: 2020/21



INSTALLATION GUIDE:

1. On your system, install the appropriate anaconda package from https://www.anaconda.com/products/individual
   and Visual Studio Code from https://code.visualstudio.com/download

2. In a directory of your choice, copy the project files folder or run in terminal(making sure git is installed);
	 git clone https://github.com/iannjari/COVID-19-Cases-and-Mortality-Analysis-and-Prediction.git

3. On anaconda prompt, create a new anaconda virtual environment by running;
	conda create --name myenv 
NOTE: Replace with your preferred name

4. On Anaconda prompt, activate the new environment using;
	conda activate myenv
NOTE: Replace with your environment's name

5. Install the following package by running the accompanying command in the new environment:

Numpy -----> conda install -c conda-forge numpy
Pandas -----> conda install -c anaconda pandas
Plotly -----> conda install -c plotly plotly
Dash ------> conda install -c conda-forge dash
Matplotlib -> conda install -c conda-forge matplotlib
Seaborn ---> conda install -c anaconda seaborn
FPDF ------> conda install -c conda-forge fpdf
Py3DNS ----> conda install -c auto py3dns
Prophet ----> conda install -c conda-forge prophet
validate_email> conda install -c conda-forge validate_email

NOTE: If an installation fails or conda gets stuck on 'solving environment', run;
	'pip install packagename' from anaconda

6. Open Visual Studio Code from the anaconda environment by running;
	code
7. When Visual Studio Code opens, open the project folder's src folder 

8. Run the following scripts in the following order:
	pre-processor.py
	report-generator.py
	predict.py
	app.py
- An application should be available at http://127.0.0.1:8050/ when 'app.py' is run successfully
- 'predict.py' is expected to run for ~23 minutes to completion.