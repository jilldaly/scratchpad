import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data(file):
    data_file = pd.ExcelFile(file)
    df = pd.read_excel(data_file, 'train')
    df = df.dropna()
    return df.X.values, df.Y.values


def visualise_relationship(x, y, title='Linear Regression - Lab 01'):
    plt.scatter(x,y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.show()
    return plt


def hypothesis(X, lambda1, bias):
    return (lambda1 * X) + bias


def residuals(X, y, lambda1, bias):
    return hypothesis(X, lambda1, bias) - y


def mse(residuals, m):
    return (np.sum(residuals**2))/m
    
 
def r_sq(residuals, sum_squares):
    return 1 - (np.sum(residuals**2)/sum_squares)    


def linear_regression_gd(X, y, gd_iters, plt):
    
    # Starting values for lr, gd
    lambda1 = 0.0
    bias = 0.0
    alpha = 0.05  
    m = len(X)
    
    # starting values for measuring the model
    sum_squares = np.sum((np.mean(y) - y)**2)
    mse_values = []
    rsq = 0
    
    for i in range(gd_iters):

        # get the errors for lambda1, bias
        errors = residuals(X, y, lambda1, bias) 
        
        # calculate gradient for lambda1, bias usimg the residuals/cost
        gradient_l = (1.0/m) * (np.sum((errors*X)))
        gradient_b = (1.0/m) * (np.sum((errors)))

        # use gradient descent rule to calculate new values for parameters
        temp_l = lambda1 - (alpha * gradient_l)
        temp_b = bias - (alpha * gradient_b)
                
        # simultaneous update of lambda1, bias
        lambda1 = temp_l
        bias = temp_b
        
        # append the errors to different metros
        mse_values.append(mse(errors, m))
        rsq = r_sq(errors, sum_squares)


    # plot improvement in MSE values 
    plt.plot(mse_values)
    plt.show()
    
    return lambda1, bias, rsq


def main():
    
    file = "data.xlsx"

    # Load the data values
    X, y = load_data(file)
    
    # Examine thge Relationship
    plt = visualise_relationship(X, y)
    
    # Standardise X
    X = (X - np.mean(X))/np.std(X)
    
    # Build the model
    lambda1, bias, rsq = linear_regression_gd(X, y, 500, plt) 
    
    print('lambda1 = ', lambda1)
    print('bias = ', bias)
    print('r sq = ', rsq)
    
    # Get the pedicted values based on the final lambda, bias
    y_predicted = hypothesis(X, lambda1, bias)
    
    # visualise the final fitted line 
    plt.scatter(X, y)
    plt.plot(X,y_predicted,'k-')
    plt.show()
    
    
main()    
