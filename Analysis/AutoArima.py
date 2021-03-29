import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pmdarima as pmd
import scipy
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_squared_error as mse

Seriesfile="./output/VTimeSeries_interpolation.xlsx"

def checkSeries(series): # numpy arrays or series
    if type(series)==pd.core.series.Series:
        series=series.to_numpy()
    pmd.tsdisplay(series)
    print(pmd.acf(series))
    pmd.plot_acf(series)
    pmd.plot_pacf(series)

def processBeforeTrans(series): # pandas series
    seriesO=series
    series=series.replace(0,1)
    seriesA=series-seriesO
    return series,seriesA

def seriesTransform(series,ctl=1,bclmbda=None): # pandas series
    if type(series)!=np.ndarray:
        series = series.to_numpy()
    if ctl==1:
        series = np.log(series)
        print(scipy.stats.normaltest(series))
        return series
    if ctl==2:
        series = series**np.e
        series = series.tolist()
        return series
    if ctl==3:
        series= scipy.stats.boxcox(series,lmbda=None)
        print(scipy.stats.normaltest(series[0]))
        return series[0]
    if ctl==4:
        series= scipy.special.inv_boxcox(series,bclmbda)
        series = series.tolist()
        return series

def getArimamodel(series):
    series_fit = pmd.auto_arima(series, start_p=1, start_q=1,
                                max_p=3, max_q=3, m=24,
                                start_P=0, seasonal=True,
                                d=1, D=1, trace=True,
                                error_action='ignore',
                                suppress_warnings=True,
                                stepwise=True)
    series_fit.summary()
    return series_fit

def getTrain_Test(series,num):
    train,test=pmd.model_selection.train_test_split(series,train_size=num)
    return train,test

def drawPrediction(train,test,predict,title="TTP"):
    x1=range(1,len(train)+len(test)+1)
    x2=range(len(train)+1,len(train)+len(test)+1)
    plt.title(title)
    plt.xlabel(f'Future Videos (RMSE={np.sqrt(mse(test, predict)):.3f})')
    plt.ylabel("Values")
    plt.plot(x1, train+test, c="b", label="$Actural$")
    plt.plot(x2, predict, c="r", label="$Predict$")
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

def checkRediduals(test,predict,title="Residuals"):
    test=np.array(test)
    predict = np.array(predict)
    residual=test-predict
    p=scipy.stats.normaltest(residual)
    plt.hist(residual, bins=15)
    plt.axvline(0, linestyle='--', c='r')
    plt.xlabel(f'Residuals (p={p.pvalue:.3f})')
    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    df = pd.read_excel(Seriesfile, sheet_name="original")
    series = df["N"]
    checkSeries(series)
    print(scipy.stats.normaltest(np.array(series)))
    # Original Time Series frequency is highly right skewed
    # ACF has long tail, seasonality is 24
    # PACF cut tail at rank 1
    # Try Log and Boxcox Transformation
    # Since there are "0"s in the data set, so we have to preprocess
    # Normaltest:statistic=249.9603717702918, pvalue=5.269809582389706e-55
    s_nozero,s_fix=processBeforeTrans(series)
    # Try Log first
    s_Log=seriesTransform(s_nozero,1)
    # Normaltest:statistic=337.3457658684751, pvalue=5.575678128353711e-74
    checkSeries(s_Log)
    # PACF seems better, and frequancy seems better too but there are still 0 values
    # Try Coxbox
    s_Cox=seriesTransform(s_nozero,3)
    # Normaltest:statistic=211.62874771001353, pvalue=1.1102002702731354e-46
    Boxcoxlmbda = 0.13369423810417647
    checkSeries(s_Cox)
    # Boxcox seems the best among them, so we predic with it
    print(len(s_Cox))
    # We save the last 24 for test and others for train
    Cox_train,Cox_test=getTrain_Test(s_Cox,480)
    Cox_fit=getArimamodel(Cox_train)
    # Best set ARIMA(3,1,0)(2,1,0)[24]
    # AIC: 992.192
    # Not too bad

    # Try Log transformation set
    Log_train,Log_test=getTrain_Test(s_Log,480)
    Log_fit=getArimamodel(Log_train)
    # Best set ARIMA(3,1,0)(2,1,0)[24]
    # AIC: 751.708
    # Seems better

    # Let's take a look at if we model with original data
    train,test=getTrain_Test(np.array(series),480)
    origin_fit=getArimamodel(train)
    # Best set ARIMA(3,1,0)(2,1,0)[24]
    # AIC: 3669.135
    # Seems not so good

    #For Log transformation has the best performance, we use it for prediction
    Log_predict = Log_fit.predict(24)
    #Transformback
    Log_train=seriesTransform(Log_train,2)
    Log_test=seriesTransform(Log_test,2)
    Log_predict=seriesTransform(Log_predict,2)
    drawPrediction(Log_train,Log_test,Log_predict,"Log_Trans_Prediction")
    checkRediduals(Log_test,Log_predict,"Log_Residuals")

    predict=origin_fit.predict(24)
    train=train.tolist()
    test = test.tolist()
    predict = predict.tolist()
    drawPrediction(train, test, predict, "Origin_Prediction")
    checkRediduals(test, predict, "Origin_Residuals")

    Cox_predict=Cox_fit.predict(24)
    Cox_train = seriesTransform(Cox_train,4,Boxcoxlmbda)
    Cox_test = seriesTransform(Cox_test,4,Boxcoxlmbda)
    Cox_predict = seriesTransform(Cox_predict,4,Boxcoxlmbda)
    drawPrediction(Cox_train, Cox_test, Cox_predict, "Coxbox_Prediction")
    checkRediduals(Cox_test, Cox_predict, "Coxbox_Residuals")

# Train model with full data and predict 24
    # Boxcox
    s_Cox1 = scipy.stats.boxcox(s_nozero, lmbda=None)
    Cox_fit = getArimamodel(s_Cox1[0])
    # Best set: ARIMA(3,1,0)(2,1,0)[24]
    # AIC: 1049.693
    Cox_predict = Cox_fit.predict(24)
    Cox_predict1 = scipy.special.inv_boxcox(np.array(Cox_predict),s_Cox1[1])
    # # Log
    Log_fix1 = getArimamodel(s_Log)
    Log_fix1.summary()
    Log_predict1 = Log_fix1.predict(24)
    Log_predict1 = np.power(Log_predict1,np.e)
    Log_predict1[np.isnan(Log_predict1)]=0
    # Lpre1=Log_fix1.predict(24)
    # Lpre1=np.power(Lpre1,np.e)
    # Lpre1[np.isnan(Lpre1)] = 0
    # Best set: ARIMA(3,1,0)(2,1,0)[24]
    # AIC: 795.041
    origin_fit1=getArimamodel(np.array(series))
    origin_fit1.summary()
    predict1=origin_fit1.predict(24)


