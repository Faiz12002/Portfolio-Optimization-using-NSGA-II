# Imports: 
import customtkinter as ctk
from customtkinter import filedialog as filedialog
import pandas as pd
import numpy as np 
import random 
import matplotlib.pyplot as plt
from fpdf import FPDF
from PIL import Image
from yac import *
# Initialize the root:
root = ctk.CTk()
# Define constants & config:
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_title = 'Portfolio Optimizer'
icon_path = 'icon.ico'
font_title = 'Helvetica Rounded'
font_normal = 'Helvetica'
font_title_size = 30
font_normal_size = 20
image = ctk.CTkImage(light_image=Image.open(icon_path), size=(180,180))
solution = ()
asset_dataframe = pd.DataFrame()
csv_path = ''
tabs = []
tabs_title = ['Main', 'Optimize', 'Settings']

txt_en = [
    'Main',
    'Optimize',
    'Settings'
]

txt_fr = [
    'Principal',
    'Optimiser',
    'Parametres'
]

# Define functions:
# ...
# Define events:
    # Open CSV file event

def load_csv():
    global asset_dataframe
    global data_display_box
    global csv_path
    csv_path = filedialog.askopenfilename(filetypes=[("CSV Files","*.csv")])
    if csv_path:
        try:
            asset_dataframe = pd.read_csv(csv_path)
            data_display_box.insert('0.0', f"{asset_dataframe.to_string(index=False, col_space=10, justify='left', header=True)}")
            data_display_box.configure(state = 'disabled')

        except IOError:
            print('Error opening file')

def random_values():
    global input_max_gen
    global input_max_pop
    global input_divd
    global input_mutation_rate
    input_max_gen.delete('0', 'end')
    input_max_pop.delete('0', 'end')
    input_divd.delete('0', 'end')
    input_mutation_rate.delete('0', 'end')
    input_max_gen.insert('0', f'{str(random.randint(100,1000))}')
    input_max_pop.insert('0', f'{str(random.randint(10,50))}')
    input_divd.insert('0', f'{str(random.randint(2,20))}')
    input_mutation_rate.insert('0', f'{str(round(random.uniform(0.001, 0.999), 3))}')


def optimization_process():
    global start_optimizing_button
    global logs_display_box
    global asset_dataframe
    global input_budget
    global plot_button
    global report_as_pdf_button
    global solution
    global logs_plot_button
    if asset_dataframe.empty or input_max_gen.get() == '' or input_max_pop.get() == '' or input_divd.get() == '' :
        logs_display_box.configure(state = 'normal')
        results_display_box.configure(state = 'normal')
        logs_display_box.delete(1.0, ctk.END)
        results_display_box.delete(1.0, ctk.END)
        if lang_comboBox.get() == 'EN':    
            logs_display_box.insert('0.0', 'MISSING VALUES: CHECK DATA IF LOADED OR FILL PARAMETERS')
            results_display_box.insert('0.0', 'REPORT CAN NOT BE WRITTEN')
        elif lang_comboBox.get() == 'FR':
            logs_display_box.insert('0.0', 'VALEURS MANQUANTES : VÉRIFIEZ LES DONNÉES SI ELLES SONT CHARGÉES OU REMPLISSEZ LES PARAMÈTRES.')
            results_display_box.insert('0.0', 'LE RAPPORT NE PEUT PAS ÊTRE CRÉE.')
        logs_display_box.configure(state = 'disabled')
        results_display_box.configure(state = 'disabled')
    else:
        if input_budget.get() == '':
            budget = 1
        else:
            budget = float(input_budget.get())
        max_gen = int(input_max_gen.get())
        max_pop = int(input_max_pop.get())
        divd = int(input_divd.get())
        t = float(input_mutation_rate.get())
        E = -np.array(asset_dataframe.mean())
        V = np.array(asset_dataframe.cov())
        start_optimizing_button.configure(state='disabled')
        solution = NSGA2(E,V,max_gen, max_pop,len(E),divd, t)
        logs_display_box.configure(state = 'normal')
        results_display_box.configure( state = 'normal')
        logs_display_box.delete(1.0, ctk.END)
        results_display_box.delete(1.0, ctk.END)
        if lang_comboBox.get() == 'EN':
            for i in range(len(solution[0])-1, -1, -1):
                logs_display_box.insert('0.0',f"Rank {i}: {str(solution[0][i])}\n")
            logs_display_box.insert('0.0', f'Mutation rate: {input_mutation_rate.get()}\n')
            logs_display_box.insert('0.0', f"Divd: {input_divd.get()}\n")
            logs_display_box.insert('0.0', f"Number of initial population: {input_max_pop.get()}\n")
            logs_display_box.insert('0.0', f"Number of generations: {input_max_gen.get()}\n")
            logs_display_box.insert('0.0', f'Budget: {budget}\n')
            logs_display_box.insert('0.0', f'Number of period returns: {len(asset_dataframe.index)}\n')
            logs_display_box.insert('0.0', f'Number of assets: {len(asset_dataframe.columns)}\n')
            for i in range(len(solution[0][0])-1,-1,-1):
                results_display_box.insert('0.0',f"Allocate {list(np.round(budget * solution[1][i],4))}, to get:\n{str(-solution[0][0][i][0])} return\n{str(solution[0][0][i][1])} risk\nBudget used: {np.round(budget * np.sum(solution[1][i]),4)}\n\n")
            results_display_box.insert('0.0', 'Budget allocations from first asset to last one\n')
            results_display_box.insert('0.0', '----- Efficient solutions given risk-return tradeoff -----\n')
        elif lang_comboBox.get() == 'FR':
            for i in range(len(solution[0])-1, -1, -1):
                logs_display_box.insert('0.0',f"Rang {i}: {str(solution[0][i])}\n")
            logs_display_box.insert('0.0', f'Taux de mutation: {input_mutation_rate.get()} \n')
            logs_display_box.insert('0.0', f"Divd : {input_divd.get()}\n")
            logs_display_box.insert('0.0', f"Nombre de population initiale : {input_max_pop.get()}\n")
            logs_display_box.insert('0.0', f"Nombre de générations : {input_max_gen.get()}\n")
            logs_display_box.insert('0.0', f'Budget : {budget}\n')
            logs_display_box.insert('0.0', f'Nombre de rendements périodiques : {len(asset_dataframe.index)}\n')
            logs_display_box.insert('0.0', f'Nombre d\'actifs : {len(asset_dataframe.columns)}\n')
            for i in range(len(solution[0][0])-1,-1,-1):
                results_display_box.insert('0.0',f"Allouer {list(np.round(budget * solution[1][i],4))}, pour obtenir :\n{str(-solution[0][0][i][0])} rendement\n{str(solution[0][0][i][1])} risque\nBudget utilisé : {np.round(budget * np.sum(solution[1][i]),4)}\n\n")
            results_display_box.insert('0.0', 'Allocations de budget du premier actif au dernier\n')
            results_display_box.insert('0.0', '----- Solutions efficaces en fonction du compromis rendement-risque -----\n')
        logs_display_box.configure(state = 'disabled')
        results_display_box.configure(state = 'disabled')
        start_optimizing_button.configure(state='normal')
        logs_plot_button.configure(state='normal')
        plot_button.configure(state='normal')
        report_as_pdf_button.configure(state='normal')
def pareto_scatterplot():
    if lang_comboBox.get() == 'EN':
        plt.scatter([x[1] for x in solution[0][0]],[-x[0] for x in solution[0][0]])
        plt.grid(True)
        plt.xlabel('Risk')
        plt.ylabel('Return')
        plt.title('Efficient frontier')
    elif lang_comboBox.get() == 'FR':
        plt.scatter([x[1] for x in solution[0][0]],[-x[0] for x in solution[0][0]])
        plt.grid(True)
        plt.xlabel('Risque')
        plt.ylabel('Rendement')
        plt.title('Frontière efficiente')
    plt.show()
def logs_scatterplot():
    if lang_comboBox.get() == 'EN':
        for i in range(len(solution[0])):
            plt.scatter([x[1] for x in solution[0][i]],[-x[0] for x in solution[0][i]], label = f"Ranks: {i}")
        plt.grid(True)
        plt.xlabel('Risk')
        plt.ylabel('Return')
        plt.legend()
    elif lang_comboBox.get() == 'FR':
        for i in range(len(solution[0])):
            plt.scatter([x[1] for x in solution[0][i]],[-x[0] for x in solution[0][i]], label = f"Rang : {i}")
        plt.grid(True)
        plt.xlabel('Risque')
        plt.ylabel('Rendement')
        plt.legend()
    plt.show()
def export_as_pdf():
    if input_budget.get() == '':
        budget = 1
    else:
        budget = float(input_budget.get())
    def space(n):
        return n*' '
    class REPORT(FPDF):
        def header(self):
            self.image(icon_path, 10, 10, 20)
            self.set_font('Helvetica','BU', 30)
            if (lang_comboBox.get() == 'EN'):
                self.cell(0,20, 'Portfolio Optimizer Report', align='C', new_x='LMARGIN', new_y='NEXT')
            elif (lang_comboBox.get() == 'FR'):
                self.cell(0,20, 'Rapport Portfolio Optimizer', align='C', new_x='LMARGIN', new_y='NEXT')
        def footer(self):
            # Page numbers in footer
            self.set_y(-15)
            self.set_font('Helvetica', 'B', 9)
            self.cell(0, 10, f'{self.page_no()}', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf = REPORT('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=30)
    pdf.set_font('Helvetica', 'B', 25)
    if lang_comboBox.get() == 'EN':
        pdf.cell(10,30, 'Given the informations below:',new_x='LMARGIN', new_y='NEXT')
    elif lang_comboBox.get() == 'FR':
        pdf.cell(10,30, 'Selon les informations ci-dessous.',new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', 'BI', 20)
    if lang_comboBox.get() == 'EN':
        pdf.cell(10,0, f'{space(1)}- Budget: {budget} DZD' , new_x='LMARGIN', new_y='NEXT')
    elif lang_comboBox.get() == 'FR':
        pdf.cell(10,0, f'{space(1)}- Budget: {budget} DZD' , new_x='LMARGIN', new_y='NEXT')
    pdf.ln(10)
    if lang_comboBox.get() == 'EN':
        pdf.cell(10,0, f'{space(1)}- Data: ' , new_x='LMARGIN', new_y='NEXT')
    elif lang_comboBox.get() == 'FR':
        pdf.cell(10,0, f'{space(1)}- Données: ' , new_x='LMARGIN', new_y='NEXT')
    pdf.ln()

    # Column widths
    col_widths = [190 / len(asset_dataframe.columns) for i in range(len(asset_dataframe))]
    pdf.ln()
    # Header row
    pdf.set_font('Helvetica', 'B', 10)
    for i, col in enumerate(asset_dataframe.columns):
        pdf.cell(col_widths[i], 10, col, 1)
    pdf.ln()

    # Data rows
    pdf.set_font('Helvetica', '', 10)
    for _, row in asset_dataframe.iterrows():
        for i, val in enumerate(row):
            pdf.cell(col_widths[i], 10, str(val), 1)
        pdf.ln()

    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 25)
    if lang_comboBox.get() == 'EN':
        pdf.cell(10,0, 'Efficient portfolio selection: ', new_x='LMARGIN', new_y='NEXT')
    elif lang_comboBox.get() == 'FR':
        pdf.cell(10,0, 'Sélection de portefeuille efficace: ', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    portfolios = []
    returns = []
    risks = []
    budget_used = []
    for i in range(len(solution[0][0])):
        portfolios.append(list(np.round(budget * solution[1][i],4)))
        returns.append(str(-solution[0][0][i][0]))
        risks.append(str(solution[0][0][i][1]))
        budget_used.append(np.round(budget * np.sum(solution[1][i]),4))
    if lang_comboBox.get() == 'EN':
        selection_dict = {'Portfolio (DZD)':portfolios, 'Return (%)':returns, 'Risk (%)':risks, 'Budget used (DZD)':budget_used}
    elif lang_comboBox.get() == 'FR':
        selection_dict = {'Portefeuille (DZD)':portfolios, 'Rendement (%)':returns, 'Risque (%)':risks, 'Budget utilisé (DZD)':budget_used}
    selection_df = pd.DataFrame(selection_dict)
    # Allocate {}
    # to get:\n{} return
    # {} risk
    # Budget used: {}
    # for i in range(len(solution[0][0])):
    #     pass
    #     pdf.cell(10,20,f"Allocate {list(np.round(budget * solution[1][i],4))}, to get:\n{str(-solution[0][0][i][0])} return\n{str(solution[0][0][i][1])} risk\nBudget used: {np.round(budget * np.sum(solution[1][i]),4)}\n\n", new_x='LMARGIN', new_y='NEXT')

    # Column widths
    col_widths = [100, 35,20,38]
    pdf.ln()
    # Header row
    pdf.set_font('Helvetica', 'B', 10)
    for i, col in enumerate(selection_df.columns):
        pdf.cell(col_widths[i], 10, col, 1)
    pdf.ln()

    # Data rows
    pdf.set_font('Helvetica', '', 10)
    for _, row in selection_df.iterrows():
        for i, val in enumerate(row):
            pdf.cell(col_widths[i], 10, str(val), 1)
        pdf.ln()
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 25)
    if lang_comboBox.get() == 'EN':
        pdf.cell(5,0, 'Efficient frontier', new_x='LMARGIN', new_y='NEXT')
    elif lang_comboBox.get() == 'FR':
        pdf.cell(5,0, 'Frontière efficiente', new_x='LMARGIN', new_y='NEXT')
    plt.scatter([x[1] for x in solution[0][0]],[-x[0] for x in solution[0][0]])
    if lang_comboBox.get() == 'EN':
        plt.xlabel('Risk')
        plt.ylabel('Return')
        plt.title('Efficient frontier')
    elif lang_comboBox.get() == 'FR':
        plt.xlabel('Risque')
        plt.ylabel('Rendement')
        plt.title('Frontière efficiente')
    plt.savefig('efficientFrontier.png')
    y_position = pdf.get_y()
    y_position += 10
    pdf.image('efficientFrontier.png', x=10, y=y_position, w=150)
    pdf.output('Report.pdf')
def show_about():
        # Create a new toplevel window
    toplevel = ctk.CTkToplevel()
    if lang_comboBox.get() == 'EN':
        toplevel.title('About')
    elif lang_comboBox.get() == 'FR':
        toplevel.title('À propos')
    toplevel.geometry("300x250")
    toplevel.resizable(0,0)
    if lang_comboBox.get() == 'EN':
        aboutDetails = """\
App: Portfolio Optimizer
Desc: Portfolio optimization using NSGA-II
Version: 2024.05.02
Python: 3.11.2
Customtkinter: 5.2.2
Github: Faiz12002, mayarhm14
    """
    elif lang_comboBox.get() == 'FR':
        aboutDetails = """\
App: Portfolio Optimizer
desc: Optimisation du portefeuille avec NSGA-II
Version: 2024.04.26
Python: 3.11.2
customtkinter: 5.2.2
Github: Faiz12002, mayarhm14
    """
    # Create a label to display the message
    label = ctk.CTkLabel(toplevel, text=aboutDetails, wraplength=250, justify = 'left')
    label.pack(padx=20, pady=10)

    # Create a button to close the toplevel window
    if lang_comboBox.get() == 'EN':
        button = ctk.CTkButton(toplevel, text='Close', command=toplevel.destroy)
    elif lang_comboBox.get() == 'FR':
        button = ctk.CTkButton(toplevel, text='Fermer', command=toplevel.destroy)
    button.pack(pady=5)

    # Run the toplevel window
    toplevel.grab_set()
    toplevel.mainloop()
def apply_changes():
    global lang_comboBox
    global TabContainer
    global txt_fr
    global tab_title
    global tabs
    if lang_comboBox.get() == 'FR':
        # Translate tab names
        for i in range(len(tabs_title)-1):
            TabContainer.rename(txt_en[i], txt_fr[i])
        walkthrough_label.configure(text = 'Guide')
        # Translate tab[0]
        AboutButton.configure(text = '')

        line1_label.configure(text = tab_txt1_fr)
        line2_label.configure(text = tab_txt2_fr)
        line3_label.configure(text = tab_txt3_fr)
        line4_label.configure(text = tab_txt4_fr)
        line5_label.configure(text = tab_txt5_fr)
        line6_label.configure(text = tab_txt6_fr)
        line61_label.configure(text = tab_txt61_fr)
        line62_label.configure(text = tab_txt62_fr)
        line7_label.configure(text = tab_txt7_fr)
        line8_label.configure(text = tab_txt8_fr)

        # Translate tab[1]

        LoadAssets_label.configure(text = 'Charger les données de vos actifs')
        open_button.configure(text = 'Charger les données')
        input_budget.configure(placeholder_text = 'Définir le budget')
        experimental_label.configure(text = 'Expérimental : Paramètres NSGA-II')
        input_max_gen.configure(placeholder_text = 'Générations maximales')
        input_max_pop.configure(placeholder_text = 'Nombre maximal initial de la population')
        input_divd.configure(placeholder_text = 'Degré de diversité')
        input_mutation_rate.configure(placeholder_text = 'Taux de mutation')
        random_params.configure(text = 'Paramètres aléatoires')
        optimize_label.configure(text = 'Optimiser')
        logs_label.configure(text = 'Journal')
        start_optimizing_button.configure(text = 'Démarrer')
        logs_plot_button.configure(text = 'Afficher le nuage de points du journal')
        plot_button.configure(text = 'Afficher la frontière efficiente')
        plot_button.place(x = 720, y = 455)
        report_as_pdf_button.configure(text = 'Exporter le rapport au format PDF')
        report_label.configure(text = 'Rapport')
    if lang_comboBox.get() == 'EN':
        # Translate tab names
        for i in range(len(tabs_title)-1):
            TabContainer.rename(txt_fr[i], txt_en[i])
        walkthrough_label.configure(text = 'Walkthrough')
        # Translate tab[0]
        AboutButton.configure(text = 'About')

        line1_label.configure(text = tab_txt1)
        line2_label.configure(text = tab_txt2)
        line3_label.configure(text = tab_txt3)
        line4_label.configure(text = tab_txt4)
        line5_label.configure(text = tab_txt5)
        line6_label.configure(text = tab_txt6)
        line61_label.configure(text = tab_txt61)
        line62_label.configure(text = tab_txt62)
        line7_label.configure(text = tab_txt7)
        line8_label.configure(text = tab_txt8)

        # Translate tab[1]

        LoadAssets_label.configure(text = 'Load your assets data')
        open_button.configure(text = 'Load data')
        input_budget.configure(placeholder_text = 'Set budget')
        experimental_label.configure(text = 'Experimental: NSGA-II Parameters')
        input_max_gen.configure(placeholder_text = 'Max generations')
        input_max_pop.configure(placeholder_text = 'Max initial population number')
        input_divd.configure(placeholder_text = 'Diversity degree')
        input_mutation_rate.configure(placeholder_text = 'Mutation rate')
        random_params.configure(text = 'Set random')
        optimize_label.configure(text = 'Optimize')
        logs_label.configure(text = 'Logs')
        start_optimizing_button.configure(text = 'Start')
        logs_plot_button.configure(text = 'Display scatterplot logs')
        plot_button.configure(text = 'Display efficient frontier')
        plot_button.place(x = 760, y = 455)
        report_as_pdf_button.configure(text = 'Export report as PDF')
        report_label.configure(text = 'Report')

# App config: 
root.title(app_title)
root.geometry(f'{screen_width}x{screen_height}+0+0')
root.iconbitmap(icon_path)
# Layout
    # Tabs container
TabContainer = ctk.CTkTabview(root)
TabContainer.pack(fill='both', ipady = 300)
for tab_title in tabs_title:
    tabs.append(TabContainer.add(tab_title))

    # Main Tab [0]
# for position, string in enumerate(tab_0_str):
#     if position == 0:
#         ctk.CTkLabel(tabs[0], text=string, font=(font_title, font_title_size)).place(x = 0, y = position*100)
#     else:
#         ctk.CTkLabel(tabs[0], text=string, font=(font_normal, font_normal_size)).place(x = 0, y = position*100)
tab_txt1 = "• In optimize tab: load your assets file as .csv, your data should be containing returns over a period of time."
tab_txt2 = "• Set your budget, when the budget is not specified, the app will simply assume proportions. "
tab_txt3 = "• The app optimizes portfolios using NSGA-II algorithm, play with the parameters to get results that suits you the most."
tab_txt4 = "• Set random parameters by clicking \"Random\" button if you are unsure what parameters to input."
tab_txt5 = "• After entering all the needed values, click \"Start\" button in \"Optimize\" section, this will start optimizing the portfolio."
tab_txt6 = "• When Logs and Report are displayed, then the optimization process returned a success."
tab_txt61 = " - Logs: Displays all the inputs about your optimization process, as well of all the solutions generated by the algorithm."
tab_txt62 = " - Report: Displays all the solutions from the efficient frontier generated by the algorithm in a structured way."
tab_txt7 = "• You can display scatterplots of all the solutions or only efficient solutions, as well as exporting the report as PDF for further use."
tab_txt8 = "• Settings tab contains app settings."

tab_txt1_fr = "• Chargez votre fichier d'actifs au format .csv dans l'onglet Optimiser, avec des rendements sur une période de temps."
tab_txt2_fr = "• Définissez un budget ; si non spécifié, l'application utilisera des proportions par défaut."
tab_txt3_fr = "• Optimisation des portefeuilles avec NSGA-II. Ajustez les paramètres pour des résultats optimaux."
tab_txt4_fr = "• Paramètres aléatoires disponibles via le bouton \"Aléatoire\" si besoin."
tab_txt5_fr = "• Cliquez sur \"Démarrer\" dans la section \"Optimiser\" pour lancer l'optimisation."
tab_txt6_fr = "• Affichage des journaux et du rapport une fois l'optimisation terminée."
tab_txt61_fr = "  - Journal: Toutes les entrées et solutions générées."
tab_txt62_fr = "  - Rapport: Frontière efficace de manière structurée."
tab_txt7_fr = "• Graphiques de dispersion disponibles. Exportez le rapport au format PDF."
tab_txt8_fr = "• Paramètres de l'application dans l'onglet Paramètres."



ctk.CTkLabel(tabs[0], text='Portfolio Optimizer', font=(font_title, font_title_size)).place(x = 490, y = 0)
AboutButton = ctk.CTkButton(tabs[0], text='', bg_color='transparent', fg_color='transparent', hover_color='#2b2b2b', border_width=0, width=150, image=image, command=show_about)
walkthrough_label = ctk.CTkLabel(tabs[0], text="Walkthrough:", font=(font_title, font_title_size))
line1_label = ctk.CTkLabel(tabs[0], text=tab_txt1, font=(font_normal, font_normal_size))
line2_label = ctk.CTkLabel(tabs[0], text=tab_txt2, font=(font_normal, font_normal_size), text_color='#049bd6')
line3_label = ctk.CTkLabel(tabs[0], text=tab_txt3, font=(font_normal, font_normal_size))
line4_label = ctk.CTkLabel(tabs[0], text=tab_txt4, font=(font_normal, font_normal_size), text_color='#049bd6')
line5_label = ctk.CTkLabel(tabs[0], text=tab_txt5, font=(font_normal, font_normal_size))
line6_label = ctk.CTkLabel(tabs[0], text=tab_txt6, font=(font_normal, font_normal_size), text_color='#049bd6')
line61_label = ctk.CTkLabel(tabs[0], text=tab_txt61, font=(font_normal, font_normal_size), text_color='#049bd6')
line62_label = ctk.CTkLabel(tabs[0], text=tab_txt62, font=(font_normal, font_normal_size), text_color='#049bd6')
line7_label = ctk.CTkLabel(tabs[0], text=tab_txt7, font=(font_normal, font_normal_size))
line8_label = ctk.CTkLabel(tabs[0], text=tab_txt8, font=(font_normal, font_normal_size), text_color='#049bd6')

    # Optimize Tab [1]
LoadAssets_label = ctk.CTkLabel(tabs[1], text='Load your assets data', font=(font_title, font_title_size))
open_button = ctk.CTkButton(tabs[1], text="Load data", command=load_csv)
input_budget = ctk.CTkEntry(tabs[1], placeholder_text='Set budget')
data_display_box = ctk.CTkTextbox(tabs[1], height=100, width=400)
experimental_label = ctk.CTkLabel(tabs[1], text='Experimental: NSGA-II Parameters', font=(font_title, font_title_size))
input_max_gen = ctk.CTkEntry(tabs[1], placeholder_text='Max generations')
input_max_pop = ctk.CTkEntry(tabs[1], placeholder_text='Max initial population number')
input_divd = ctk.CTkEntry(tabs[1], placeholder_text ='Diversity degree')
input_mutation_rate = ctk.CTkEntry(tabs[1], placeholder_text='Mutation rate')
random_params = ctk.CTkButton(tabs[1], text='Set random', command=random_values)
optimize_label = ctk.CTkLabel(tabs[1], text='Optimize', font = (font_title, font_title_size))
start_optimizing_button = ctk.CTkButton(tabs[1], text='Start', width=150, height=30, command=optimization_process)
logs_label = ctk.CTkLabel(tabs[1], text='Logs', font=(font_normal, font_normal_size))
logs_display_box = ctk.CTkTextbox(tabs[1], height=200, width=600)
logs_plot_button = ctk.CTkButton(tabs[1], text='Display scatterplot logs', command=logs_scatterplot)
report_label = ctk.CTkLabel(tabs[1], text='Report', font = (font_title, font_title_size))
results_display_box = ctk.CTkTextbox(tabs[1], height=400, width=500)
plot_button = ctk.CTkButton(tabs[1], text='Display efficient frontier', command=pareto_scatterplot)
report_as_pdf_button = ctk.CTkButton(tabs[1], text='Export report as PDF', command=export_as_pdf)

    # Main Tab [2]
    # needs
    # combo boxes
    # two combo boxes, one for theme and one for translation then a button of apply changes
ctk.CTkLabel(tabs[2], text='Language preferences', font=(font_title, font_title_size)).place(x = 470, y = 0)
lang_comboBox = ctk.CTkComboBox(tabs[2], values=['EN', 'FR'], state='readonly')
lang_comboBox.set('EN')
apply_changes_button = ctk.CTkButton(tabs[2], text='Apply changes', command=apply_changes)
# Widgets config:
walkthrough_label.place(x = 0, y = 70)
line1_label.place(x = 0, y = 120)
line2_label.place(x = 0, y = 170)
line3_label.place(x = 0, y = 220)
line4_label.place(x = 0, y = 270)
line5_label.place(x = 0, y = 320)
line6_label.place(x = 0, y = 370)
line61_label.place(x = 50, y = 400)
line62_label.place(x = 50, y = 430)
line7_label.place(x = 0, y = 480)
line8_label.place(x = 0, y = 530)

AboutButton.place(x = 1050, y = 0)
LoadAssets_label.place(x = 0, y = 0)
experimental_label.place(x = 0, y = 200)
optimize_label.place(x = 0, y = 300)
logs_label.place(x = 0, y = 350)
open_button.place(x = 0, y = 50)
report_label.place(x = 900, y = 0)
input_budget.place(x = 150, y = 50)
data_display_box.place(x=0, y=100)
input_max_gen.place(x = 0, y = 250)
input_max_pop.place(x = 150, y = 250)
input_divd.place(x = 300, y = 250)
input_mutation_rate.place(x = 450, y = 250)
random_params.place(x = 450, y = 280)
start_optimizing_button.place(x = 250, y = 350) 
logs_plot_button.place(x = 450, y = 350)
logs_plot_button.configure(state='disabled')
logs_display_box.place(x = 0, y = 380)
results_display_box.place(x = 700, y = 50)
results_display_box.configure(state='disabled')
plot_button.place(x = 760, y = 455)
plot_button.configure(state='disabled')
report_as_pdf_button.place(x = 950, y = 455)
report_as_pdf_button.configure(state='disabled') 
lang_comboBox.place(x = 560, y = 50)
apply_changes_button.place(x = 560, y = 90)





# Run the app
root.mainloop()