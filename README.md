![GitHub](https://img.shields.io/github/license/till-teb/expenses-management-tool)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/till-teb/expenses-management-tool/main.yml)

# expenses-management-tool
Management tool to analyse, visualize and forecast expenses.

### More detailed description:

This program consists of a data generator for generating sample data, which has to be started separately, and the finance tool, with which it is possible to track and visualize one's finances by input itself.

Inputs via the financial tool are saved as a CSV file in the user's own database directory and can be displayed and modified in the financial tool for your own analysis purposes in the form of plots and as a data frame.

## Installation and run

### loca:
Download and install:   
```
git clone https://github.com/till-teb/expenses-management-tool.git  
cd expenses-management-tool  
pip install -r requirements.txt  
```

Then:  
- enter subfolder  
- run:   
```
streamlit run expenses.py  
```

### Streamlit Cloud:

[https://expenses-tool.streamlit.app/](https://expenses-tool.streamlit.app/) [experimental]  

Although the app is visible, certain functions like storing or deleting data cannot be used. This is because the app relies on a local path to access the CSV file for the dataset. When the app is run on the Streamlit Cloud, it cannot find the local path on the device, resulting in an error.

## How to use
### App:
When the management tool is started, you have the option on the sidebar to choose from various windows for entering expenses, recurring expenses, recurring income including additional income, and the dashboard for visualization. To make entries for a specific topic, you need to navigate through the respective input windows and fill out the separate form for the selected topic.

In all input windows, it is possible to edit or delete the entries at any time after saving the selection. Additionally, it is also possible to record previous expenses or income and display the entire dataset as a dataframe in the respective window.

When selecting the dashboard on the sidebar, an additional dropdown menu is available to select the specific topic, target month, and year to display. In the dashboard itself, regardless of the topic selected, the current financial status for the selected period is always displayed at the top in the form of a horizontal bar plot. This shows the income and expenses compared to each other, giving an idea of one's financial capacity.

Under this plot, the total income and total expenses for the selected period are calculated separately.

The second plot shows the financial performance of one's own balance, making it possible to visualize the history of the period in the form of a line plot. Additionally, the current balance for the period is displayed below this plot.

Next, the dataset can be found as a dataframe, which displays the topic and the total amount for the selected time frame.

In the last section, the user has the option to choose a more detailed category representation of the percentage distribution of their finances and a corresponding more detailed visualization of the emotional state and importance of their expenses over their chosen period.

The emotional and importance details are visualized in the form of two bar plots, each showing their distribution. Additionally, the most frequently occurring emotional state and the median distribution of importance are displayed below.

When selecting the category details, the percentage distribution of categories is displayed in the form of two pie charts for the selected topics of expenses and recurring expenses. The first plot shows the distribution of categories. By selecting a dropdown menu, you can also choose to display the subcategories of the categories over the period.

Since no subcategories exist for the topic income, the distribution of individual categories without subcategories is displayed in the form of a bar plot for the selected topic.

All plots update themselves with every new input, showing the overall financial trend over the period.

### Data-Generator:

The data generator can create example data in a CSV file format, which is then automatically stored in the "datasets" subfolder. You can view, modify, or delete the example data in the app whenever needed.
To use the data generator, you must first navigate to the subdirectory where it is located within the downloaded "expenses management tool" directory and then run it.

```
cd expenses-management-tool
```
- enter subfolder  
- run:   

```
python data_generator.py
```

If the generator does not work, you must create your own example.