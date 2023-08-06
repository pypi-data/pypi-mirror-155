#Importing libraries
import numpy as np
import pandas as pd
from numpy.random import seed
import tensorflow as tf 
from keras import Sequential
from keras.layers import Dense

# setting the seed
seed(0)
tf.random.set_seed(0)

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#Loading datasets: monthly data

#Setting file paths
directory_path = "/content/drive/MyDrive/IME 699/datasets"

z_50_filepath =  directory_path + "/c_50.csv"
r_50_1_filepath = directory_path + "/r1_50.csv"
r_50_2_filepath = directory_path + "/r2_50.csv"
z_100_filepath = directory_path + "/c_100.csv"
r_100_1_filepath = directory_path + "/r1_100.csv"
r_100_2_filepath = directory_path + "/r2_100.csv"

## Case 1: Pc = 50
z_50 = pd.read_csv(z_50_filepath, header=None)
# model (a)
r_50_1 = pd.read_csv(r_50_1_filepath, header=None)
x_train_50_1, x_test_50_1, y_train_50_1, y_test_50_1 = train_test_split(z_50, r_50_1, test_size = 1/3, shuffle=False) 
# model (b)
r_50_2 = pd.read_csv(r_50_2_filepath, header=None)
x_train_50_2, x_test_50_2, y_train_50_2, y_test_50_2 = train_test_split(z_50, r_50_2, test_size = 1/3, shuffle=False)

##Case 2: Pc = 100
z_100 = pd.read_csv(z_100_filepath, header=None)
# model (a)
r_100_1 = pd.read_csv(r_100_1_filepath, header=None)
x_train_100_1, x_test_100_1, y_train_100_1, y_test_100_1 = train_test_split(z_100, r_100_1, test_size = 1/3, shuffle=False)  
# model (b)
r_100_2 = pd.read_csv(r_100_2_filepath, header=None)
x_train_100_2, x_test_100_2, y_train_100_2, y_test_100_2 = train_test_split(z_100, r_100_2, test_size = 1/3, shuffle=False) 

#Custom R2 for stocks
def squared_error(y, y_hat):
  return sum((y-y_hat)**2)

def r2_score(y_real, y_pred):
  num = squared_error(y_real, y_pred)
  den = squared_error(y_real, 0) 
  return 1-(num/den)[0]

"""**Increasing width and fixed depth**"""

# defining architecture
def wide_nn(input_dim, hidden_units, initializer='he_normal', lrate_val=0.0001):
  model = tf.keras.models.Sequential()
  # Input layer
  model.add(tf.keras.layers.Input(shape=(input_dim, )))
  # 2 Hidden layers
  model.add(tf.keras.layers.Dense(hidden_units, activation='relu', kernel_initializer=initializer))
  model.add(tf.keras.layers.Dense(hidden_units, activation='relu', kernel_initializer=initializer))
  # Output layer
  model.add(tf.keras.layers.Dense(1, activation='linear', kernel_initializer=initializer))
  model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lrate_val), metrics=['mse'])
  return model

#Define experiments
def wide_experiment(x_train, y_train, x_test, y_test, input_dim, hidden_units, epochs=100, batchsize=128):
  model = wide_nn(input_dim, hidden_units)
  model.fit(x_train, y_train, epochs=epochs, batch_size=batchsize, verbose=0)
  y_train_prediction, y_test_prediction = model.predict(x_train), model.predict(x_test)
  is_r2, oos_r2 = r2_score(y_train.to_numpy(), y_train_prediction), r2_score(y_test.to_numpy(), y_test_prediction)
  is_mse, oos_mse = mean_squared_error(y_train, y_train_prediction), mean_squared_error(y_test, y_test_prediction)
  return is_r2, oos_r2, is_mse, oos_mse  

# widths
widths = [0, 1, 3, 5, 7, 9, 10, 20, 30, 40, 45, 47, 49, 50, 51, 53, 55, 60, 70, 80, 90, 100, 110, 130, 150, 170, 200, 250, 256, 512, 1024]

wide_is_r2_50_1, wide_oos_r2_50_1, wide_is_mse_50_1, wide_oos_mse_50_1 = [], [], [], []
for hidden_unit in widths:
  is_r2_val, oos_r2_val, is_mse_val, oos_mse_val = wide_experiment(x_train_50_1, y_train_50_1, x_test_50_1, y_test_50_1, input_dim=100, hidden_units=hidden_unit)
  wide_is_r2_50_1.append(is_r2_val)
  wide_oos_r2_50_1.append(oos_r2_val)
  wide_is_mse_50_1.append(is_mse_val)
  wide_oos_mse_50_1.append(oos_mse_val)
wide_df_50_1 = pd.DataFrame({"IS_R2": wide_is_r2_50_1, "OOS_R2": wide_oos_r2_50_1, "IS_MSE": wide_is_mse_50_1, "OOS_MSE": wide_oos_mse_50_1})

wide_is_r2_50_2, wide_oos_r2_50_2, wide_is_mse_50_2, wide_oos_mse_50_2 = [], [], [], []
for hidden_unit in widths:
  is_r2_val, oos_r2_val, is_mse_val, oos_mse_val = wide_experiment(x_train_50_2, y_train_50_2, x_test_50_2, y_test_50_2, input_dim=100, hidden_units=hidden_unit)
  wide_is_r2_50_2.append(is_r2_val)
  wide_oos_r2_50_2.append(oos_r2_val)
  wide_is_mse_50_2.append(is_mse_val)
  wide_oos_mse_50_2.append(oos_mse_val)
wide_df_50_2 = pd.DataFrame({"IS_R2": wide_is_r2_50_2, "OOS_R2": wide_oos_r2_50_2, "IS_MSE": wide_is_mse_50_2, "OOS_MSE": wide_oos_mse_50_2})

wide_is_r2_100_1, wide_oos_r2_100_1, wide_is_mse_100_1, wide_oos_mse_100_1 = [], [], [], []
for hidden_unit in widths:
  is_r2_val, oos_r2_val, is_mse_val, oos_mse_val = wide_experiment(x_train_100_1, y_train_100_1, x_test_100_1, y_test_100_1, input_dim=200, hidden_units=hidden_unit)
  wide_is_r2_100_1.append(is_r2_val)
  wide_oos_r2_100_1.append(oos_r2_val)
  wide_is_mse_100_1.append(is_mse_val)
  wide_oos_mse_100_1.append(oos_mse_val)
wide_df_100_1 = pd.DataFrame({"IS_R2": wide_is_r2_100_1, "OOS_R2": wide_oos_r2_100_1, "IS_MSE": wide_is_mse_100_1, "OOS_MSE": wide_oos_mse_100_1})

wide_is_r2_100_2, wide_oos_r2_100_2, wide_is_mse_100_2, wide_oos_mse_100_2 = [], [], [], []
for hidden_unit in widths:
  is_r2_val, oos_r2_val, is_mse_val, oos_mse_val = wide_experiment(x_train_100_2, y_train_100_2, x_test_100_2, y_test_100_2, input_dim=200, hidden_units=hidden_unit)
  wide_is_r2_100_2.append(is_r2_val)
  wide_oos_r2_100_2.append(oos_r2_val)
  wide_is_mse_100_2.append(is_mse_val)
  wide_oos_mse_100_2.append(oos_mse_val)
wide_df_100_2 = pd.DataFrame({"IS_R2": wide_is_r2_100_2, "OOS_R2": wide_oos_r2_100_2, "IS_MSE": wide_is_mse_100_2, "OOS_MSE": wide_oos_mse_100_2})

wide_results_50_1 =  directory_path + "/wide_results_50_1.csv"
wide_results_50_2 =  directory_path + "/wide_results_50_2.csv"
wide_results_100_1 =  directory_path + "/wide_results_100_1.csv"
wide_results_100_2 =  directory_path + "/wide_results_100_2.csv"

wide_df_50_1.to_csv(wide_results_50_1)
wide_df_50_2.to_csv(wide_results_50_2)
wide_df_100_1.to_csv(wide_results_100_1)
wide_df_100_2.to_csv(wide_results_100_2)