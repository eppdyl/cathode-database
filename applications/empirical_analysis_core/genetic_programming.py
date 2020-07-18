# MIT License
# 
# Copyright (c) 2020 Pierre-Yves Taunay 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''
File: genetic_programming.py
Author: Pierre-Yves Taunay
Date: 2020

Attempt to use genetic programming to find an expression that links the Pi
products for the total pressure together.
'''
def genetic_programming(pidata):
    if plot_gp:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import MinMaxScaler
        from sympy import init_printing
        
        init_printing(use_latex=True,forecolor="White")
        
    #    Y = np.array(pidata['PI1'])
    #    X = np.array(pidata[['PI2','PI3','PI4','PI5','PI6','PI7']])

        XY = np.array(pidata)
        min_max_scaler = MinMaxScaler()
        min_max_scaler.feature_range = (0.1,1)
        XY_train_minmax = min_max_scaler.fit_transform(XY)
        
        Y = XY_train_minmax[:,0]
        X = XY_train_minmax[:,1:]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)

    #    xm = np.min(X_train[:,2])
    #    xM = np.max(X_train[:,2])
    ##    X_train[:,2] = (X_train[:,2] - xm) / (xM-xm)
    ##    X_train[:,2] *= 1e-12
    ##    X_train[:,4] *= 1e12
    #
    #    xm = np.min(X_train[:,4])
    #    xM = np.max(X_train[:,4])
    ##    X_train[:,4] = (X_train[:,4] - xm) / (xM-xm)    
        
        
        def _powf(x1,x2):        
            with np.errstate(over='ignore'):
                return np.where(np.abs(x1**x2) < 100, x1**x2, 0.)

            
        
        powf = make_function(function=_powf,
                            name='powf',
                            arity=2)
        
        function_set = ['add', 'sub', 'mul', 'div',
                        'neg', 'inv']
        
        est_gp = SymbolicRegressor(population_size=5000,
                                   generations=20, 
    #                               tournament_size=50,
                                   stopping_criteria=0.01,
                                   const_range = (-10,10),
                                   init_depth = (2,10),
                                   function_set=function_set,
    #                               p_crossover=0.7, 
    #                               p_subtree_mutation=0.05,
    #                               p_hoist_mutation=0.1, 
    #                               p_point_mutation=0.1,
    #                               max_samples=0.9, 
                                   verbose=1,
    #                               feature_names = ('\Pi_2','\Pi_3','\Pi_4','\Pi_5','\Pi_6','\Pi_7'),
    #                               parsimony_coefficient=0.01, 
                                   random_state=0,
                                   n_jobs=1
                                   )
        est_gp.fit(X_train, Y_train)
     
        from sympy import symbols, Add, Mul, Lambda, sympify
        import sympy as sp

        
        x,y = symbols('x y')
        loc = {
            "add": Add,
            "mul": Mul,
            "sub": Lambda((x, y), x - y),
            "div": Lambda((x, y), x/y),
            "sqrt": Lambda(x,sp.sqrt(sp.Abs(x))),
            "neg": Lambda(x,-x),
            "inv": Lambda(x,1/x),
            "powf": Lambda((x, y),x**y),
            "log": Lambda(x,sp.log(x)),
            "abs": Lambda(x,sp.Abs(x))
        }
        exp = sympify(est_gp._program,locals=loc)

        score_gp = est_gp.score(X_test, Y_test)
        print(exp)    
        print(score_gp)

        fres = []
        for row in pidata.iterrows():
            drow = row[1]
            X0 = (drow['PI2']- np.min(pidata[['PI2']])) / (np.max(pidata[['PI2']])-np.min(pidata[['PI2']]))
            X1 = (drow['PI3']- np.min(pidata[['PI3']]))/ (np.max(pidata[['PI3']])-np.min(pidata[['PI3']])) 
            X2 = (drow['PI4']- np.min(pidata[['PI4']]))/ (np.max(pidata[['PI4']])-np.min(pidata[['PI4']])) 
            X3 = (drow['PI5']- np.min(pidata[['PI5']]))/ (np.max(pidata[['PI5']])-np.min(pidata[['PI5']])) 
            X4 = (drow['PI6']- np.min(pidata[['PI6']]))/ (np.max(pidata[['PI6']])-np.min(pidata[['PI6']]))
            X5 = (drow['PI7']- np.min(pidata[['PI7']]))/ (np.max(pidata[['PI7']])-np.min(pidata[['PI7']]))
            tmp = exp.subs({'X0':X0,'X1':X1,'X2':X2,'X3':X3,'X4':X4,'X5':X5})
            fres.append(tmp)
        fres = np.array(fres)
        dPi = np.max(pidata[['PI1']]) - np.min(pidata[['PI1']])
        plt.loglog(fres,(pidata[['PI1']]-np.min(pidata[['PI1']]))/dPi,'ko')
    #    plt.xlim([0.5,1e5])
    #    plt.ylim([0.5,1e5])
        plt.loglog(np.logspace(0,5),np.logspace(0,5),'k--')

    #    print(est_gp._program)
        
    #    y_gp = est_gp.predict(np.c_[x0.ravel(), x1.ravel()]).reshape(x0.shape)
    #    score_gp = est_gp.score(X_test, y_test)
        
