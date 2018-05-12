# xgboost调参详解
# 第一步：确定学习速率和tree_based 参数调优的估计器数目

from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV

xgb1 = XGBClassifier(
    learning_rate=0.1,
    n_estimators=1000,
    max_depth=5,
    min_child_weight=1,
    gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    nthread=4,
    scale_pos_weight=1)

# 第二步： max_depth 和 min_weight 参数调优
# grid_search参考 :
# http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html
# http://blog.csdn.net/abcjennifer/article/details/23884761
# 网格搜索scoring=’roc_auc’只支持二分类，多分类需要修改scoring(默认支持多分类)

param_test1 = {'max_depth': [4, 5, 6], 'min_child_weight': [4, 5, 6]}

gsearch1 = GridSearchCV(estimator = xgb1, param_grid = param_test1,
                        scoring = 'roc_auc', n_jobs = 4,
                        iid = False, cv = 5)

gsearch1.fit(train[predictors], train[target])
gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_

# 第三步：gamma参数调优

param_test3 = {'gamma': [i / 10.0 for i in range(0, 5)]}
gsearch3 = GridSearchCV(estimator = xgb1,
                        param_grid = param_test3,
                        scoring = 'roc_auc',
                        n_jobs = 4,
                        iid = False,
                        cv = 5)
gsearch3.fit(train[predictors], train[target])
gsearch3.grid_scores_, gsearch3.best_params_, gsearch3.best_score_

# 第四步：调整subsample 和 colsample_bytree 参数
# 取0.6,0.7,0.8,0.9作为起始值

param_test4 = {'subsample': [i / 10.0 for i in range(6, 10)],
               'colsample_bytree': [i / 10.0 for i in range(6, 10)]
              }

gsearch4 = GridSearchCV(estimator = xgb1,
                        param_grid = param_test4,
                        scoring = 'roc_auc',
                        n_jobs = 4,
                        iid = False,
                        cv = 5)
gsearch4.fit(train[predictors], train[target])
gsearch4.grid_scores_, gsearch4.best_params_, gsearch4.best_score_

# 第六步：降低学习速率

xgb4 = XGBClassifier(
learning_rate = 0.01,
n_estimators = 5000,
max_depth = 4,
min_child_weight = 6,
gamma = 0,
subsample = 0.8,
colsample_bytree = 0.8,
reg_alpha = 0.005,
objective = 'binary:logistic',
nthread = 4,
scale_pos_weight = 1,
seed = 27)
modelfit(xgb4, train, predictors)

# 第六步：正则化参数调优
param_test6 = {'reg_alpha': [1e-5, 1e-2, 0.1, 1, 100]}
gsearch6 = GridSearchCV(estimator = xgb1,
                        param_grid = param_test6,
                        scoring = 'roc_auc',
                        n_jobs = 4,
                        iid = False,
                        cv = 5)
gsearch6.fit(train[predictors], train[target])
gsearch6.grid_scores_, gsearch6.best_params_, gsearch6.best_score_

