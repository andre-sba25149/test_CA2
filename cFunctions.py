# Function code to perform single or simple exponential smoothing
def single_exp_smoothing(x, alpha):
    F = [x[0]]                                  # first value is same as series
    for t in range(1, len(x)):                  # for loop for all values stored in x
        F.append(alpha * x[t] + (1 - alpha) * F[t - 1])
    return F
    
    
# Method for double exponential smoothing
def double_exp_smoothing(x, alpha, beta):
    yhat = [x[0]]
    for t in range(1, len(x)):
        if t==1:
            F, T= x[0], x[1] - x[0]
        F_n_1, F = F, alpha*x[t] + (1-alpha)*(F+T)
        T=beta*(F-F_n_1)+(1-beta)*T
        yhat.append(F+T)
    return yhat
    
# Method to initialise the values
def initialize_T(x, seasonLength):
    total=0.0
    for i in range(seasonLength):
        total+=float(x[i+seasonLength]-x[i])/seasonLength
    return total

# Method to initialise seasonality
def initialize_seasonalilty(x, seasonLength):
    seasons={}
    seasonsMean=[]
    num_season=int(len(x)/seasonLength)
    
    for i in range(num_season):
        seasonsMean.append(sum(x[seasonLength*i:seasonLength*i+seasonLength])/float(seasonLength))    
    
    for i in range(seasonLength):
        tot=0.0
        for j in range(num_season):
            tot+=x[seasonLength*j+i]-seasonsMean[j]
        seasons[i]=tot/num_season
    return seasons

# Method to write Triple exponential smoothing
def triple_exp_smoothing(x, seasonLength, alpha, beta, gamma):
    yhat=[]
    S = initialize_seasonalilty(x, seasonLength)
    for i in range(len(x)):
        if i == 0:
            F = x[0]
            T = initialize_T(x, seasonLength)
            yhat.append(x[0])
            continue
        if i >= len(x):
            m = i - len(x) + 1
            yhat.append((F + m*T) + S[i%seasonLength])
        else:
            obsval = x[i]
            F_last, F= F, alpha*(obsval-S[i%seasonLength]) + (1-alpha)*(F+T)
            T = beta * (F-F_last) + (1-beta)*T
            S[i%seasonLength] = gamma*(obsval-F) + (1-gamma)*S[i%seasonLength]
            yhat.append(F+T+S[i%seasonLength])
    return yhat