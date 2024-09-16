import csv
import pandas as pd
import matplotlib.pyplot as plt

def export_to_csv(dependencies, file_name='dependencies.csv'):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Dependency'])
        for dep in dependencies:
            writer.writerow(dep)

def export_to_excel(dependencies, file_name='dependencies.xlsx'):
    df = pd.DataFrame(dependencies, columns=['File', 'Dependency'])
    df.to_excel(file_name, index=False)

def export_to_pdf(dependencies, file_name='dependencies.pdf'):
    df = pd.DataFrame(dependencies, columns=['File', 'Dependency'])
    df.to_html('dependencies.html')
    plt.figure(figsize=(10, 5))
    plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    plt.axis('off')
    plt.savefig(file_name, format='pdf')
