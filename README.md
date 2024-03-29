## Capstone Project: Cryptocurrency forecasting and Technical Indicator Analysis

<div style="text-align: justify">

### Overview and Problem Statement

This project attempts to visualize, analyze and forecast the trends of 6 cryptocurrencies and also look for the ideal technical indicators to use in a trading environment. As cryptocurrencies are a relatively new and highly volatile asset class, it is fairly difficult for the common layperson, without the data and resources that an established financial institution can provide, to be able to learn and trade cryptocurrencies effectively and identify / formulate a good trading strategy.

The 6 chosen cryptocurrencies are as follows:

- Bitcoin (BTC)
- Ethereum (ETH)
- Litecoin (LTC)
- Stellar Lumens (XLM)
- Dash (DASH)
- Chainlink (LINK)

The first 3 cryptocurrencies are older, more established coins that are more likely to be familiar to the layperson. As these are older coins, we can make some assumptions on their price trends (e.g., correlation to each other), and also collect more price data from them. For our 3 latter cryptocurrencies, these are newer and would more likely be independent from one another, and contain less data for us to evaluate. 

Technical indicators are heuristic or pattern-based signals produced by calculating the price, volume, and/or open interest of a security or contract used by traders who follow technical analysis. By analyzing historical data, technical analysts use indicators to predict future price movements. 

### Approach and Success Metrics

The bulk of this project will be based on two concurrent machine learning models, the first being a regressor based forecasting model to predict future prices and the second being a collection of classifier based models to determine and rank the best technical indicators. There is also a third Deep Learning model, using an LSTM neural network to see if an unsupervised learning model, measured by accuracy scores, can perform betther than the classifier models. 

Due to the volatility of cryptocurrencies, one shouldn't expect high accuracy scores for any the models used in this project. The success metrics I have set are to establish a pattern for our forecasting model and any improvement over baseline scores, however small, for our classifier models. The models are structured such that I can revisit them in the future and tinker with new models and methods, as well as add new data, to improve the scores.

### Data Collection and Feature Engineering

The first step would be to collect and prepare our data. Fortunately for cryptocurrencies there are many free resources that allow you to do this. Our data source comes from an API provided by [Coinbase Pro](https://pro.coinbase.com), a well-known broker of cryptocurrencies. After creating a free account, the API allows you to download a set amount of data per given timeframe so you would have to wrap an iterative function in Python to tell the API to continuously download your datasets until you have the necessary amount.

For each of our 6 cryptocurrencies, we have a tabular dataset that consists of hourly price observations of each coin against the US Dollar across 5 columns that should be familiar to traders:

- Open
- High
- Low
- Close
- Volume Traded

Then, you would also need to find a way to calculate your technical Indicators based on your OHLCV data. Fortunately there exists a Python package that does this for us automatically, called `ta`, which provides us with 83 total technical indicators across 5 categories:

- Volume
- Volatility
- Trend
- Momentum
- Other

The datasets are then saved in a csv, or better yet, an SQL database (local).

### Exploratory Data Analysis

The EDA can be helpful here to visualize how a trader would typically analyze the trends and patterns of each coin. Our datasets, which are organized in hourly intervals can be resampled to show daily intervals instead, technical indicators included. With `plotly`, we can view the charts and make our own qualitative inferences for each coin. 

See the charts in the EDA notebook in this [NBViewer page](https://nbviewer.jupyter.org/github/marzimin/Project-1-Cryptocurrencies/tree/master/).

### Model 1: ARIMA Models for 5 day forecasts

Our first model is the ARIMA based regressor models, constructed with a Python package called `pmdarima`, which allows you to construct your models in a `sklearn` style format. I have also added other evaluation metrics in addition to the model, as well as a 120 hour (5 day) forecast, based on the model predictions of the close price, for each coin. You can then choose your selection of technical indicators (our exogenous features) and re-run the model multiple times to see how it performs. 

The evaluation metrics are as follows:

- Stationarity checks (for close and chosen exogenous features)
- Model summary scores
- Autocorrelation and Partial Autocorrelation graphs
- Your model projections compared to actual results
- Residual plots
- RMSE plots

### Model 2: Classifier based models for Technical Indicator Analysis

Our second classification models will evaluate our 83 technical indicators (or features) to find which one (or group) would be best suited to fit our ARIMA models. Unlike the regressor model, some minor feature engineering needs to be made for these models:

- Shift all columns by 1 period forward
	- This is so that the technical indicators from the previous period are used as your feature variables

- Create a binary column showing a price increase (1) or decrease/no change (0) (This is your target variable)

- Drop the open, high, low, close, volume columns so that only technical indicators are used.

The classifier models used here vary from:

- Logistic Regression
- Support Vector Machine
- Decision Trees
- Bagging Methods (Random Forests)
- Boosting Methods (Gradient Boosting)
- Naive Bayes (GaussianNB)
- Neural Network (sklearn MLP)

The goal here is to see which classifier type is best suited for cryptocurrencies where we can rank their accuracy scores and find the feature importances (our technical indicators).

### Model 3: LSTM Neural Networks

I have added a third, minor part to this project that goes over the implementation of a TensorFlow + Keras model to identify if a Deep Learning model can outperform the prior classification models in predicting binary price movements of our cyptocurrencies. With the data loaded and preprocessed similarly to the earlier models, the TensorFlow model here consists of 200 epochs, and constructed with 3 LSTM layers, followed by 6 Dense layers, each layer halving from an initial 512 nodes to our binary outputs. The model is tracked and measured by its accuracy and loss on the predictions generated from both the train and validation (test sets).
### Results

As expected the accuracy scores for the first two models aren't that great, showing only a similar pattern that generally undervalues the predicted prices in the ARIMA models and a ~5% improvement over baseline scores in the classifier models. This is also not taking into account of the larger fluctuations of cryptocurrencies throughout the month of February, with volatility exceeding previous periods that are in this dataset. Regarding the most important technical indicators, we are able to identify a handful of the most important ones per coin but not to a highly signifcant degree to have them stand out from the other indicators.

As for the LSTM model, it appears that the scores also did not improve much from baseline and performed similarly to our classifier models, averaging a ~5% improvement on their test sets. More model tinkering, in addition to new data would be needed.

### Key Learnings

It remains tough to estimate the price trends of a volatile asset class such as cryptocurrencies but the caveat is that it leaves room for one to explore other models, datasets, and even external features that may affect price trends. For instance, implementing new features derived from natural language processing methods, one example being where there is heightened traffic of people discussing the coins on social media and its effects on price. Other examples to explore could include other indexes such as gold or foreign exchanges to increase the amount of data that we can analyse. Overall it was a good learning experience for someone who wants to get into machine learning and cryptocurrency trends.

**Required Dependencies**

See the requirements.txt file for more specifics

- NumPy
- Pandas
- Matplotlib
- Seaborn
- Plotly
- Scikit-learn
- [Cbpro](https://pypi.org/project/cbpro/)
- [ta](https://github.com/bukosabino/ta)
