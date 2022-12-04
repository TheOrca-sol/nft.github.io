
from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import login_required, current_user

from sqlalchemy.sql import func

import json

from . import db
from .models import User,Trade
#import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st

 

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
# Create data
    #x=range(1,6)
    #y=[1,4,6,8,4]

# Area plot
    #plt.fill_between(x, y)
    #plt.show()
   
    if request.method == 'POST':
        projectName = request.form.get('projectName')
        buy = request.form.get('buy')
        

        sell = request.form.get('sell')

        fees = request.form.get('fees')

        rsltFees = (float(sell)*float(fees))/100
        format_rsltFees = "{:.2f}".format(rsltFees)

        profit = float(sell)-float(buy)-rsltFees
        format_profit = "{:.2f}".format(profit) 

        profitPercent= (profit/float(sell))*100
        format_profitPercent = "{:.2f}".format(profitPercent) 

        roi = float(sell)/float(buy)
        format_roi = "{:.2f}".format(roi)
          

        roiPercent = (float(sell)/float(buy)*100)-100
        format_roiPercent = "{:.2f}".format(roiPercent)

        new_trade = Trade(buy=buy,sell=sell,projectName=projectName,fees=fees,profit=format_profit,profitPercent=format_profitPercent,roi=format_roi,roiPercent=format_roiPercent,user_id=current_user.id)
        db.session.add(new_trade)
        db.session.commit()
        
        flash('Trade added!', category='success')
    else:
        flash('Trade not added!', category='error')
    #tbuy = sum(Trade.buy)
    totalProfitQuery=db.session.query(func.sum(Trade.profit))
    totalBuyQuery=db.session.query(func.sum(Trade.buy))
    totalSellQuery=db.session.query(func.sum(Trade.sell))
    totalProfit = db.session.execute(totalProfitQuery).fetchall()
    totalBuy = db.session.execute(totalBuyQuery).fetchall()
    totalSell = db.session.execute(totalSellQuery).fetchall()
    totalRoiCountQuery=db.session.query(func.count(Trade.roi))
    totalRoiCount = db.session.execute(totalRoiCountQuery).fetchall()
    totalRoiSumQuery=db.session.query(func.sum(Trade.roi))
    totalRoiSum = db.session.execute(totalRoiSumQuery).fetchall()
    #totalRoi = int(totalRoiSum) / int(totalRoiCount)
    
    return render_template("home.html",totalProfit=totalProfit[0],totalBuy=totalBuy[0],totalSell=totalSell[0], user=current_user)

@views.route('/chart', methods=['GET','POST'])
@login_required
def chart():
    income_vs_expenses = db.session.query(db.func.sum(Trade.buy),db.func.sum(Trade.sell))

    income_expense = []
    for total_Profit, _ in income_vs_expenses:
        income_expense.append(total_Profit)

    expenses = db.session.query(db.func.sum(Trade.sell),db.func.sum(Trade.buy))
    ttl_expense=[]
    for total_expense, _ in expenses:
        ttl_expense.append(total_expense)

    dates = db.session.query(db.func.sum(Trade.profit), Trade.date).group_by(Trade.date).order_by(Trade.date).all()
    dates_labels = []
    over_time=[]
    for prf, date in dates:
        over_time.append(prf)
        dates_labels.append(date.strftime("%d-%m-%y"))

    datesTrdC = db.session.query(db.func.count(Trade.buy), Trade.date)
    dates_trade = []
    trade_count=[]
    for tradeC, dateT in datesTrdC:
        trade_count.append(tradeC)
        dates_trade.append(dateT.strftime("%d-%m-%y"))
    return render_template("chart.html",
    income_vs_expenses = json.dumps(income_expense),
    expenses = json.dumps(ttl_expense),
    over_time = json.dumps(over_time),
    dates= json.dumps(dates_labels),
    trade_count = json.dumps(trade_count),
    datesTrdC= json.dumps(dates_trade),
    user=current_user)

@views.route('/delete-trade', methods=['POST'])
def delete_trade():
    trade = json.loads(request.data)
    tradeId = trade['tradeId']
    trade = Trade.query.get(tradeId)
    if trade:
        if trade.user_id == current_user.id:

            db.session.delete(trade)
            db.session.commit()
    return jsonify({})

@views.route('/addRaid', methods=['GET','POST'])
@login_required
def addRaid():
    return render_template("addRaid.html",user=current_user)