from __future__ import annotations
import numpy as np
from sklearn.linear_model import LinearRegression



class SmoothingAndPredict():    
    def correct(self, X_raw, y_raw, graph=False) : 
        y = y_raw.copy()
        X = X_raw.copy()
        while True :  
            reg = LinearRegression().fit(X.T, y)                
            score = reg.score(X.T,y)
            pred = reg.predict(X.T)
            
            error = pred - y 
            error_mean = np.mean(error)
            error_std = np.std(error)            
            
            idx_boolean = (error >= error_mean +  max(1.96 * error_std, 3)) | (error <= error_mean -  max(1.96 * error_std, 3))
            print("\tFitting by regression model")
            print("\t\t- R^2: {}, mean: {}, std: {}".format(round(score,3), round(error_mean,3), round(error_std,3)))
            idx = np.where(idx_boolean == True )[0]
            y[idx] = pred[idx] 
            if len(idx) == 0 :            
                break
        return y
    
    def validate(self, y, X) :                               
        corrected_y = self.correct(X,y)                                    
        suspected_timesteps = sorted(np.where(abs(y - corrected_y)>3)[0])                   
        print("\nFound noise by new model\n\t", suspected_timesteps)       
        print(y-corrected_y)                        
        print("\n")            
        return suspected_timesteps
