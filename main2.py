
import webbrowser
from fpdf import FPDF
from flask.views import MethodView
from wtforms import Form ,StringField,SubmitField
from flask import Flask,render_template,request,send_file


class Bill:
    """object that contains data about a bill such as total amount and period of the bill"""

    def __init__(self, amount, period):
        self.period = period
        self.amount = amount

class Flatmate:
    """creates a flatmate person who lives in
     the flat and pays a share of the bill"""

    def __init__(self,name,days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self,bill,flatmate2):
        k = self.days_in_house/(self.days_in_house + flatmate2.days_in_house)
        to_pay = bill.amount * k
        return to_pay
class PdfReport:
    """crates a pdf file that contains data about such
    as their name ,due amount and period of the bill"""

    def __init__(self,filename):
        self.filename = filename
    def generate(self,flatmate1,flatmate2,bill):
        flatmate2_debt = str(round(flatmate2.pays(bill,flatmate2=flatmate1),2))
        flatmate1_debt = str(round(flatmate1.pays(bill,flatmate2=flatmate2),2))
        pdf = FPDF()
        pdf.add_page()
        #add the title
        pdf.set_font(family="Times", size=24, style="B")
        pdf.cell(w=0, h=80, txt="Flatmates Bill", border=0, align="C", ln=1)
        #insert period lable and value
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=100, h=40, txt="Period:", border=0)
        pdf.cell(w=150, h=40, txt=bill.period, border=0,ln=1)

        #insert name and due amount of first flatmate
        pdf.cell(w=100, h=40, txt=flatmate2.name, border=0)
        pdf.cell(w=150, h=40, txt=flatmate2_debt + "dollars", border=0,ln =1 )
        #insert name and due amount of other flatmate
        pdf.cell(w=100, h=40, txt=flatmate1.name, border=0)
        pdf.cell(w=150, h=40, txt=flatmate1_debt + "dollars", border=0)
        pdf.output(self.filename)
        webbrowser.open(self.filename)

app =Flask(__name__)



class HomePage(MethodView):
    
    def get(self):
        return render_template("index.html")

class BillFormPage(MethodView):
    
    def get(self): 
        bill_form = BillForm()
        return render_template("bill_form_page.html" , billform = bill_form)



@app.route("/download" ,methods = ["POST"])
def download():
    
    
    billform = BillForm(request.form)
    amount = float(billform.amount.data)
    period = billform.period.data


    name1 = billform.name1.data
    days_in_the_house1 = float(billform.days_in_the_house1.data)


    name2 = billform.name2.data
    days_in_the_house2 = float(billform.days_in_the_house2.data)

        
    the_bill =Bill(amount , period)
            
        
    Mate1 = Flatmate(name1 , days_in_the_house1)
            
    
    Mate2 = Flatmate(name2 , days_in_the_house2)
    pdf_report = PdfReport("Yourreport.pdf")
    pdf_report.generate(Mate1,Mate2,the_bill)
        
        
    return send_file(pdf_report , as_attachment=True , download_name="Yourreport.pdf")






class BillForm(Form):
    amount = StringField("Bill Amount: ")
    period =  StringField("Bill Period: ")
    name1 = StringField("Name: ")
    days_in_the_house1 = StringField("Number of days spent in the house:")
    name2 = StringField("Name: ")
    days_in_the_house2 = StringField("Number of days spent in the house:")

    button = SubmitField("Get pdf")

    



    

app.add_url_rule("/",view_func= HomePage.as_view("home_page"))
app.add_url_rule("/bill_form",view_func= BillFormPage.as_view("bill_form_page"))




app.run(debug=True)