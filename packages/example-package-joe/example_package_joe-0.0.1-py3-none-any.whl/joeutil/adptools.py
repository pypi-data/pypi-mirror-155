from scipy import stats
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')

__version__ = 0.01
colors = sns.color_palette('Set1')
markers = ['o', 's', '^', 'P', 'D', 'H', 'x']
gParams = {
    'func': None, 'round': 3, 'target': None, 'verbose': False,
    'sort': True, 'by': 'dtypes', 'ascending': False, 'filter': False,
    'plot': False, 'cols': 5, 'figsize': (12, 5), 'cmap': plt.cm.Set1, 'color': colors[0], 'width': 0.3, 'palette': 'Set1', 'alpha': 0.6, 'rotation': 90,
    'kind': 'kde', 'shade': True, 'bins': 10,
}

#########################################################################################################
# 유틸리티 - util
#########################################################################################################


def dir():
    print(' # 샘플 데이터 : load_data / boston|cancer|iris|titanic|diabetes')
    print(' # 변수 구성 : features')
    print(' # 변수별 데이터 : info')
    print(' # 숫자형 변수 통계 : describe(T) / kde|hist|box')
    print(' # 볌주형 변수 통계 : count(N), countone(1)')
    print(' # 데이터 상관관계 : corr')
    print(' # 결측치, 이상치 : na, outlier')
    print(' # 종속독립 상관관계 : xcorr(T)')
    print(' # 독립변수 중요도 : ximportance(T)')
    print(' # 독립변수 다중공선성 : xvif')
    print(' # 시각화 - 분포 : plt_dist(T) / kde|hist|box')
    print(' # 시각화 - 2차원 : plt_2xdim(T) / svd|pca')
    print(' # 데이터 샘플링 : pre_sampling(T) / ros|smote|rus')
    print(' # 데이터 분리(X,y) : pre_split(T)')
    print(' # 데이터 스케일링 : pre_scale(X) / minmax|standard|log')
    print(' # 최적 모델 탐색 : model_search / cls|reg')
    print(' # 교차 검증 : cv_score, cv_reg_score, cv_cls_score')
    print(' # 데이터프레임 소수점 제거 : util_round')
    print(' # 컬럼 순서 변경 : util_movecols(C, T) / firts|last')
    print(' # 상관관계 : util_lambda(명목형), util_gamma(순서형)')


def init_params(lParams, **kargs):
    params = gParams.copy()
    params.update(lParams)
    params.update(kargs)
    if params['verbose']:
        print(params)
    return params


def util_movecols(columns, target, position):
    cols = list(columns)
    cols.remove(target)
    if position == 'first':
        cols.insert(0, target)
    elif position == 'last':
        cols.append(target)
    return cols


# 범주형 상관관계 / 명목형
def util_lambda(crosstab):
    max_column = np.max(crosstab.sum(axis=0))
    denominator = np.sum(crosstab.sum()) - max_column
    numerator = 0
    for i in range(len(crosstab)):
        max_row = np.max(crosstab.iloc[i, :])
        numerator = numerator + np.sum(crosstab.iloc[i, :]) - max_row
    return util_round(numerator/denominator, 4)



# 범주형 상관관계 / 순서형
def util_gamma(crosstab):
    n_row, n_col = crosstab.shape[0], crosstab.shape[1]
    P, Q = 0, 0
    for i in range(n_row-1):
       for j in range(n_col-1):
           standard = crosstab.iloc[i, j]
           concordant = crosstab.iloc[i+1:, j+1:]
           P = P + np.sum(np.sum(concordant*standard))
    for i in sorted(np.arange(1, n_col), reverse=True):
        for j in range(n_row-1):
            standard = crosstab.iloc[j, i]
            discordant = crosstab.iloc[j+1:, :i]
            Q = Q+np.sum(np.sum(discordant*standard))
    return (P-Q)/(P+Q)


def util_round(df, round=3):
    rtn = df.copy()
    types = rtn.dtypes.values
    for i, c in enumerate(rtn.columns):
        if str(types[i]).find('float') >= 0:
            rtn[c] = np.round(df[c], round)
    rtn.fillna('', inplace=True)
    return rtn


from sklearn.datasets import load_boston, load_breast_cancer, load_iris
def load_data(data_name):
    if data_name == 'boston':
        boston = load_boston()
        df_boston = pd.DataFrame(
            data=boston.data, columns=boston.feature_names)
        df_boston['target'] = boston.target
        df = df_boston
    elif data_name == 'cancer':
        cancer = load_breast_cancer()
        df_cancer = pd.DataFrame(
            data=cancer.data, columns=cancer.feature_names)
        df_cancer['target'] = cancer.target
        df = df_cancer
    elif data_name == 'iris':
        iris = load_iris()
        df_iris = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df_iris['target'] = iris.target
        df_iris.columns = ['sepal_length', 'sepal_width',
                           'petal_length', 'petal_width', 'target']
        df = df_iris
    elif data_name == 'mtcars':
        df_mtcars = pd.read_csv(
            'https://github.com/ksky1313/ADP/raw/main/data/mtcars.csv')
        df_mtcars['target'] = df_mtcars['qsec']
        df = df_mtcars.iloc[:, 1:]
    elif data_name == 'diabetes':
        df_diabetes = pd.read_csv(
            'https://raw.githubusercontent.com/ksky1313/ADP/main/data/adp22_Q1.csv')
        df_diabetes.rename(columns={'Outcome': 'target'}, inplace=True)
        df = df_diabetes
    elif data_name == 'titanic':
        df_titanic = pd.read_csv(
            'https://raw.githubusercontent.com/ksky1313/ADP/main/data/titanic.csv')
        df_titanic.rename(columns={'Survived': 'target'}, inplace=True)
        df = df_titanic.iloc[:, 2:]
    else:
        print('Unknown Data Name')
        return
    X, y = df.iloc[:, :-1], df.iloc[:, -1]
    return df, X, y.values


#########################################################################################################
# 데이터 탐색 - eda
#########################################################################################################
def features(df, **kargs):
    params = init_params({'func': 'features'}, **kargs)
    rtn = pd.DataFrame(data=df.dtypes.value_counts(), columns=['dtypes'])
    for i in rtn.index:
        cols = list(df.dtypes[df.dtypes.apply(lambda x: x in [i])].index)
        rtn.loc[i, 'columns'] = ', '.join(cols)
    if params['plot']:
        rtn['dtypes'].plot.barh(figsize=params['figsize'], cmap=params['cmap'],
                                color=params['color'], width=params['width'], alpha=params['alpha'])
        plt.show()
    return rtn


def info(df, **kargs):
    params = init_params({'func': 'info'}, **kargs)
    rtn = pd.DataFrame(
        data={'dtypes': [ str(y) for x, y in df.dtypes.items() ],
              'count': np.round(df.count().values, params['round']),
              'nunique': np.round(df.nunique().values, params['round']),
              'nduplicate': np.round(df.count().values-df.nunique().values, params['round']),
              'na': np.round(df.isna().sum().values, params['round'])},
        index=df.columns)
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        rtn.plot.bar(figsize=params['figsize'], cmap=params['cmap'],
                     width=params['width'], alpha=params['alpha'])
        plt.xticks(rotation=params['rotation'])
        plt.show()
    return rtn


def describe(df, **kargs):
    params = init_params(
        {'func': 'describe', 'by': 'dtypes', 'sort':True, 'ascending': True}, **kargs)
    num_cols = list(df.dtypes[df.dtypes.apply(
        lambda x: x in ['int32', 'int64', 'float32', 'float64'])].index)
    columns = num_cols if params['filter'] else df.columns
    rtn = pd.DataFrame(
        data={'dtypes': [ str(y) for x, y in df[columns].dtypes.items() ]},
        index=columns)
    for c in columns:
        isnum = df[c].dtypes not in ['object', 'category']
        Q3, Q1 = df[c].quantile([.75, .25]) if isnum else [0, 0]
        rtn.loc[c, 'skew'] = np.round(stats.skew(
            df[~df[c].isna()][c]), params['round']) if isnum else ''
        rtn.loc[c, 'Kurtosis'] = np.round(stats.kurtosis(
            df[~df[c].isna()][c], fisher=True), params['round']) if isnum else ''
        rtn.loc[c, 'mean'] = np.round(
            df[c].mean(), params['round']) if isnum else ''
        rtn.loc[c, 'std'] = np.round(
            df[c].std(), params['round']) if isnum else ''
        rtn.loc[c, 'max'] = np.round(
            df[c].max(), params['round']) if isnum else ''
        rtn.loc[c, 'Q3'] = np.round(Q3, params['round']) if isnum else ''
        rtn.loc[c, 'Q2'] = np.round(
            df[c].median(), params['round']) if isnum else ''
        rtn.loc[c, 'Q1'] = np.round(Q1, params['round']) if isnum else ''
        rtn.loc[c, 'min'] = np.round(
            df[c].min(), params['round']) if isnum else ''
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot'] and len(num_cols) > 0:
        plt_dist(df[num_cols], params=params)
    return rtn


def count(df, **kargs):
    params = init_params(
        {'func': 'count', 'kind': 'pie', 'nunique': 10}, **kargs)
    rtn = info(df)
    for i, c in enumerate(df.columns):
        rtn.loc[c, 'freq'] = df[c].value_counts().nlargest(1).index[0]
        rtn.loc[c, 'nfreq'] = df[c].value_counts().nlargest(1).values[0]
    if params['filter']:
        rtn = rtn.loc[rtn['nunique'] <= params['nunique'], :]
    if params['plot']:
        ncol = params['cols'] if rtn.shape[0] > params['cols'] else rtn.shape[0]
        nrow = 1 if ncol < params['cols'] else int(np.ceil(rtn.shape[0]/ncol))
        _, ax = plt.subplots(nrow, ncol, figsize=(
            params['figsize'][0], 3*nrow))
        for i, c in enumerate(rtn.index):
            if nrow == 1 and ncol == 1:
                axs = ax
            else:
                axs = ax[i % ncol] if nrow == 1 else ax[int(i/ncol), i % ncol]
            if df[c].nunique() > params['nunique']:
                axs.text(0.08, 0.05, f'{c}\n\nnunique: {df[c].nunique()}')
                axs.grid(False)
                continue
            elif params['kind'] == 'bar':
                tmp = df[c].value_counts()
                sx = sns.countplot(x=df[c], alpha=params['alpha'],
                                  color=params['color'], palette=params['palette'], ax=axs)
                sx.bar_label(container=sx.containers[0], labels=tmp.values)
                sx.set(ylabel=None)
            elif params['kind'] == 'pie':
                tmp = df[c].value_counts()
                axs.pie(x=tmp.values, labels=tmp.index, colors=sns.color_palette('pastel'), 
                        autopct='%.2g%%', startangle=90, wedgeprops={'width': 0.8})
                axs.set_title(c)
        plt.tight_layout()
        plt.show()
    return rtn


def countone(X, **kargs):
    params = init_params(
        {'func': 'countone', 'plot':True, 'kind':'bar', 'ax': None, 'figsize':(8,5), 'title':'Class Count'}, **kargs)
    cat = pd.Series(data=X)
    tmp = cat.value_counts()
    rtn = pd.DataFrame(data=tmp.values, index=tmp.index, columns=['count'])
    rtn['count%'] = np.round(
        rtn['count'] / cat.shape[0] * 100, params['round'])
    if params['sort']:
        rtn = rtn.sort_index()
    if params['plot']:
        if params['ax']:
            ax = params['ax']
            if params['kind'] == 'pie':
                ax.pie(x=tmp.values, labels=tmp.index, colors=sns.color_palette('Set2'),
                    autopct='%.2f%%', startangle=90, wedgeprops={'width': 0.8})
            else:
                sx = sns.countplot(X, alpha=params['alpha'],
                    color=params['color'], palette=params['palette'], ax=ax)
                sx.bar_label(container=sx.containers[0], labels=tmp.values)
            ax.set_title(params['title'])
        else:
            plt.figure(figsize=params['figsize'])
            if params['kind'] == 'pie':
                plt.pie(x=tmp.values, labels=tmp.index, colors=sns.color_palette('Set2'),
                    autopct='%.2f%%', startangle=90, wedgeprops={'width': 0.8})
            else:
                sx = sns.countplot(X, alpha=params['alpha'],
                    color=params['color'], palette=params['palette'])
                sx.bar_label(container=sx.containers[0], labels=tmp.values)
            plt.title(params['title'])
    return rtn


def corr(df, **kargs):
    params = init_params({'func': 'corr', 'palette': 'RdBu',
                         'ncorr': 0.5, 'by': 'corr'}, **kargs)
    df_cor = df.corr()
    corrs = []
    for i, c in enumerate(df_cor.columns):
        for j, r in enumerate(df_cor.index):
            if i == j:
                break
            if np.abs(df_cor.loc[r, c]) >= params['ncorr'] and df_cor.loc[r, c] != 1:
                corrs.append([r, c, df_cor.loc[r, c]])
    rtn = pd.DataFrame(data=corrs, columns=['col1', 'col2', 'corr'])
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        plt.figure(figsize=params['figsize'])
        sns.heatmap(data=df_cor, annot=True, vmax=1, vmin=-
                    1, cmap='RdBu', linewidths=.5, fmt='.2g')
        plt.show()
    return rtn


def na(df, **kargs):
    params = init_params(
        {'func': 'na', 'by': 'na', 'title': 'Missing values'}, **kargs)
    rtn = pd.DataFrame(
        data={'dtypes': [ str(y) for x, y in df.dtypes.items() ],
              'count': np.round(df.count().values, params['round']),
              'na': np.round(df.isna().sum().values, params['round'])},
        index=df.columns)
    rtn['na(%)'] = np.round(rtn['na']/df.shape[0]*100, params['round'])
    if params['filter']:
        rtn = rtn.loc[rtn[rtn.na > 0].index, :]
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        plt.figure(figsize=params['figsize'])
        plt.bar(rtn.index, rtn.na,
                color=params['color'], width=params['width'], alpha=params['alpha'])
        for i in range(rtn.shape[0]):
            if rtn.iloc[i, 2] > 0:
                plt.text(
                    i, rtn.iloc[i, 2], f'{rtn.iloc[i, 2]:.0f}', ha='center', color='r')
        plt.xticks(rotation=params['rotation'])
        plt.title(params['title'])
        plt.show()
    return rtn


def outlier(df, **kargs):
    params = init_params(
        {'func': 'outlier', 'by': 'noutlier', 'title': 'Outlier'}, **kargs)
    rtn = pd.DataFrame(
        data={'dtypes': [ str(y) for x, y in df.dtypes.items() ],
              'count': df.count().values},
        index=df.columns)
    for c in df.columns:
        isnum = df[c].dtypes not in ['object', 'category']
        Q3, Q1 = df[c].quantile([.75, .25]) if isnum else [0, 0]
        UL, LL = Q3+1.5*(Q3-Q1), Q1-1.5*(Q3-Q1)
        rtn.loc[c, 'noutlier'] = df.loc[(df[c] < LL) | (
            df[c] > UL), c].count() if isnum else 0
        rtn.loc[c, 'noutlier(%)'] = np.round((df.loc[(df[c] < LL) | (
            df[c] > UL), c].count()/df[c].count())*100, params['round']) if isnum else ''
        rtn.loc[c, 'top'] = np.round(
            Q3+1.5*(Q3-Q1), params['round']) if isnum else ''
        rtn.loc[c, 'max'] = np.round(
            df[c].max(), params['round']) if isnum else ''
        rtn.loc[c, '50%'] = np.round(
            df[c].median(), params['round']) if isnum else ''
        rtn.loc[c, 'min'] = np.round(
            df[c].min(), params['round']) if isnum else ''
        rtn.loc[c, 'bottom'] = np.round(
            Q1-1.5*(Q3-Q1), params['round']) if isnum else ''
        rtn.loc[c, 'ntop'] = np.sum(df[c] > UL) if isnum else ''
        rtn.loc[c, 'nbottom'] = np.sum(df[c] < LL) if isnum else ''
        rtn.loc[c, 'zero'] = np.round(
            df[df[c] == 0].shape[0], params['round']) if isnum else ''
        rtn.loc[c, 'minus'] = np.round(
            df[df[c] < 0].shape[0], params['round']) if isnum else ''
    if params['filter']:
        rtn = rtn.loc[rtn[rtn.noutlier > 0].index, :]
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        plt.figure(figsize=params['figsize'])
        plt.bar(rtn.index, rtn.noutlier,
                color=params['color'], width=params['width'], alpha=params['alpha'])
        for i in range(rtn.shape[0]):
            if rtn.iloc[i, 2] > 0:
                plt.text(
                    i, rtn.iloc[i, 2], f'{rtn.iloc[i, 2]:.0f}', ha='center', color='r')
        plt.xticks(rotation=params['rotation'])
        plt.title(params['title'])
        plt.show()
    return rtn

from sklearn.preprocessing import OrdinalEncoder
def xcorr(df, **kargs):
    params = init_params({'func': 'xcorr', 'by': 'spearmanr', 'target_dtype': None,
                         'filter': True, 'title': 'Feature correlation'}, **kargs)
    if params['target'] == None:
        print('Target을 지정하세요.')
        return
    tmp = df[df[params['target']].notna()].copy()
    tmp = tmp[util_movecols(tmp.columns, params['target'], 'last')]
    column_type = []
    for c in tmp.columns:
        typ = 'cat' if tmp[c].dtypes in ['object', 'category'] else 'num'
        column_type.append(typ)
        if typ == 'cat':
            tmp[c] = OrdinalEncoder().fit_transform(tmp[[c]])
    if params['target_dtype']:
        column_type[-1] = params['target_dtype']
    rtn = pd.DataFrame(
        data={'dtypes': column_type[:-1]}, index=tmp.columns[:-1])
    for i, c in enumerate(tmp.columns[:-1]):
        tmp_c = tmp[tmp[c].notna()]
        if column_type[-1] == 'num' and column_type[i] == 'num':
            rtn.loc[c, 'pearsonr'] = np.round(stats.pearsonr(
                tmp_c[params['target']], tmp_c[c])[0], params['round'])
        else:
            rtn.loc[c, 'pearsonr'] = 0
        rtn.loc[c, 'spearmanr'] = np.round(stats.spearmanr(
            tmp_c[params['target']], tmp_c[c])[0], params['round'])
        rtn.loc[c, 'kendalltau'] = np.round(stats.kendalltau(
            tmp_c[params['target']], tmp_c[c])[0], params['round'])
        if params['filter'] == False:
            if column_type[-1] == 'cat' and column_type[i] == 'cat':
                crosstab = pd.crosstab(
                    columns=tmp_c[params['target']], index=tmp_c[c])
                _, pvalue, _, _ = stats.chi2_contingency(
                    crosstab, correction=False)
                rtn.loc[c, 'chi2_pvalue'] = np.round(pvalue, params['round'])
                rtn.loc[c, 'lambda'] = np.round(
                    util_lambda(crosstab), params['round'])
                rtn.loc[c, 'gamma'] = np.round(
                    util_gamma(crosstab), params['round'])
            else:
                rtn.loc[c, 'chi2_pvalue'] = 0
                rtn.loc[c, 'lambda'] = 0
                rtn.loc[c, 'gamma'] = 0
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        rtn.plot.bar(figsize=params['figsize'], cmap=params['cmap'],
                     width=params['width'], alpha=params['alpha'])
        plt.xticks(rotation=params['rotation'])
        plt.title(params['title'])
        plt.show()
    return rtn


def ximportance(df, **kargs):
    params = init_params({'func': 'ximportance', 'by': 'mean', 'target': None,
                         'estimator': None, 'title': 'Feature importance TOP 10'}, **kargs)
    if params['target'] == None or params['estimator'] == None:
        print('필수인자 : target, estimator(cls|reg)')
        return
    tmp = df.dropna()
    tmp = tmp[util_movecols(tmp, params['target'], 'last')]
    for c in tmp.columns:
        if tmp[c].dtypes in ['object', 'category']:
            tmp[c] = OrdinalEncoder().fit_transform(tmp[[c]])
    X, y = tmp.iloc[:, :-1], tmp.iloc[:, -1]
    if params['estimator'] == 'cls':
        model1 = DecisionTreeClassifier(
            max_depth=5, criterion='entropy').fit(X, y)
        model2 = RandomForestClassifier(
            n_estimators=100, max_depth=5, criterion='entropy').fit(X, y)
        model3 = XGBClassifier(
            n_estimators=100, eval_metric='merror').fit(X, y)
        model4 = LGBMClassifier(n_estimators=100).fit(X, y)
    else:
        model1 = DecisionTreeRegressor(
            max_depth=5).fit(X, y)
        model2 = RandomForestRegressor(
            n_estimators=100, max_depth=5).fit(X, y)
        model3 = XGBRegressor(n_estimators=100).fit(X, y)
        model4 = LGBMRegressor(n_estimators=100).fit(X, y)
    rtn = pd.DataFrame(
        data={model1.__class__.__name__: pre_scale(model1.feature_importances_, 'minmax'),
              model2.__class__.__name__: pre_scale(model2.feature_importances_, 'minmax'),
              model3.__class__.__name__: pre_scale(model3.feature_importances_, 'minmax'),
              model4.__class__.__name__: pre_scale(model4.feature_importances_, 'minmax')},
        index=X.columns)
    rtn['mean'] = rtn.mean(axis=1)
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        rtn.iloc[:10, :-1].plot.bar(figsize=params['figsize'], cmap=params['cmap'],
                                    width=params['width'], alpha=params['alpha'])
        plt.xticks(rotation=params['rotation'])
        plt.title(params['title'])
        plt.show()
    return rtn

    
from statsmodels.stats.outliers_influence import variance_inflation_factor

def xvif(df, **kargs):
    params = init_params({'func': 'xvif', 'by': 'vif',
                         'title': 'Variance inflation factor'}, **kargs)
    tmp = df.dropna()
    tmp = tmp[list(df.dtypes[df.dtypes.apply(lambda x: x in [
                   'int32', 'int64', 'float32', 'float64'])].index)]
    rtn = pd.DataFrame(
        data=[variance_inflation_factor(tmp.values, i)
              for i in range(tmp.shape[1])],
        columns=['vif'],
        index=tmp.columns)
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        rtn.plot.bar(figsize=params['figsize'], cmap=params['cmap'],
                     width=params['width'], alpha=params['alpha'])
        plt.xticks(rotation=params['rotation'])
        plt.title(params['title'])
        plt.show()
    return rtn


#########################################################################################################
# 데이터 시각화
#########################################################################################################
def plt_dist(df, params=None, **kargs):
    params = init_params(params if params else {'func': 'plt_dist'}, **kargs)
    X = df.drop(columns=list(df.dtypes[df.dtypes.apply(
        lambda x: x not in ['int32', 'int64', 'float32', 'float64'])].index))
    if params['target']:
        X[params['target']] = df[params['target']]
        X = X[util_movecols(X.columns, params['target'], 'last')]
        Xcols = X.shape[1]-1
    else:
        Xcols = X.shape[1]
    assert(Xcols >= 0)
    ncol = params['cols'] if Xcols > params['cols'] else Xcols
    nrow = 1 if ncol < params['cols'] else int(np.ceil(Xcols/ncol))
    if params['kind'] == 'box':
        X.plot(kind='box', subplots=True, layout=(nrow, ncol),
               color=params['color'], figsize=(params['figsize'][0], 3*nrow))
    else:
        _, ax = plt.subplots(nrow, ncol, figsize=(
            params['figsize'][0], 3*nrow))
        sns.set(font_scale=0.8)
        for i, f in enumerate(X.columns):
            if f == params['target']:
                continue
            if nrow == 1 and ncol == 1:
                axs = ax
            else:
                axs = ax[i % ncol] if nrow == 1 else ax[int(i/ncol), i % ncol]
            if params['kind'] == 'kde':
                if params['target']:
                    p = sns.histplot(data=X, x=f, kde=True, stat='density', hue=params['target'], alpha=params['alpha'], color=params['color'],
                                     palette=params['palette'], bins=params['bins'], multiple='stack', ax=axs)
                else:
                    p = sns.histplot(data=X, x=f, kde=True, stat='density', alpha=params['alpha'], color=params['color'],
                                     palette=params['palette'], bins=params['bins'], multiple='stack', ax=axs)
            elif params['kind'] == 'hist':
                if params['target']:
                    p = sns.histplot(data=X, x=f, hue=params['target'], alpha=params['alpha'], color=params['color'],
                                     palette=params['palette'], bins=params['bins'], multiple='stack', stat='count', ax=axs)
                else:
                    p = sns.histplot(data=X, x=f, alpha=params['alpha'], color=params['color'],
                                     palette=params['palette'], bins=params['bins'], multiple='stack', stat='count', ax=axs)
            if i > 0:
                p.legend([], [], frameon=False)
            p.set_xlabel(f, fontsize=10)
            p.set(ylabel=None)
    plt.tight_layout()
    plt.show()

from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA

def plt_2xdim(df, **kargs):
    params = init_params({'func': 'decompress', 'method': 'svd', 'target': None,
                         'title': '2D Visualize', 'ax': None, 'size': 30}, **kargs)
    tmp = df.copy()
    if params['target']:
        tmp = tmp[util_movecols(df.columns, params['target'], 'last')]
        X, y = tmp.iloc[:, :-1], tmp.iloc[:, -1]
    else:
        X, y = tmp, None
    if params['method'] == 'svd':
        comp = TruncatedSVD(n_components=2).fit_transform(X)
    else:
        comp = PCA(n_components=2).fit_transform(X)
    if params['plot']:
        if params['ax']:
            ax = params['ax']
            ax.set_title(params['title'])
        else:
            ax = plt
            plt.figure(figsize=params['figsize'])
            plt.title(params['title'])
        if params['target']:
            groups = np.unique(y)
            for i, g in enumerate(groups):
                idx = np.where(y == g)
                ax.scatter(comp[idx, 0], comp[idx, 1], s=params['size'],
                           color=colors[i], alpha=params['alpha'], label=str(g))
            ax.legend()
        else:
            hb = ax.hexbin(df.sepal_length, df.sepal_width, gridsize=50, cmap='binary')
            cb = ax.colorbar(hb)
    return comp


#########################################################################################################
# 데이터 전처리
#########################################################################################################
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler, SMOTE
def pre_sampling(df, target, method='smote'):
    tmp = df[util_movecols(df, target, 'last')]
    if method == 'ros':
        rtn, y = RandomOverSampler().fit_resample(tmp.iloc[:,:-1], tmp[target])
    elif method == 'smote':
        rtn, y = SMOTE().fit_resample(tmp.iloc[:,:-1], tmp[target])
    elif method == 'rus':
        rtn, y = RandomUnderSampler().fit_resample(tmp.iloc[:,:-1], tmp[target])
    rtn[target] = y
    return rtn

from sklearn.preprocessing import MinMaxScaler, StandardScaler, PowerTransformer
def pre_scale(df, method, pre=None, degree=None, intercept=True):
    if str(df.__class__).find('DataFrame') >= 0:
        if pre == 'ordinal':
            scaled_data = df.copy()
            for c in scaled_data.columns:
                scaled_data[c] = OrdinalEncoder(
                ).fit_transform(scaled_data[[c]])
        elif pre == 'onehot':
            scaled_data = pd.get_dummies(df, drop_first=True)
        else:
            scaled_data = df[df.dtypes[df.dtypes.apply(
                lambda x: x in ['int32', 'int64', 'float32', 'float64'])].index].copy()
    else:
        scaled_data = np.array(df).reshape(-1, 1) if df.ndim == 1 else df
    if method == 'minmax':
        scaled_data = MinMaxScaler().fit_transform(scaled_data)
    elif method == 'standard':
        scaled_data = StandardScaler().fit_transform(scaled_data)
    elif method == 'power':
        scaled_data = PowerTransformer(
            method='yeo-johnson').fit_transform(scaled_data)
    elif method == 'log':
        scaled_data = np.log1p(np.array(scaled_data))
    if degree:
        scaled_data = PolynomialFeatures(
            degree=degree, include_bias=intercept).fit_transform(scaled_data)
    return scaled_data.ravel() if df.ndim == 1 else scaled_data

def pre_split(df, target):
    tmp = df.copy()
    X = tmp.drop(columns=target)
    y = tmp[target].values
    return X, y


#########################################################################################################
# 모델 탐색
#########################################################################################################
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import statsmodels.api as sm
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import (AdaBoostClassifier, AdaBoostRegressor,
                              ExtraTreesClassifier, ExtraTreesRegressor,
                              GradientBoostingClassifier,
                              GradientBoostingRegressor,
                              HistGradientBoostingClassifier,
                              RandomForestClassifier, RandomForestRegressor)
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import (Lasso, LinearRegression, LogisticRegression,
                                  Ridge, SGDRegressor)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from xgboost import XGBClassifier, XGBRegressor

reg_estimators = [
    LinearRegression(fit_intercept=True),
    RandomForestRegressor(n_estimators=100, max_depth=5),
    XGBRegressor(n_estimators=100),
    LGBMRegressor(n_estimators=100),
    Lasso(alpha=0, max_iter=100),
    Ridge(alpha=1, max_iter=100),
    ExtraTreesRegressor(n_estimators=100),
    GradientBoostingRegressor(n_estimators=100),
    DecisionTreeRegressor(max_depth=5),
    AdaBoostRegressor(),
    MLPRegressor(max_iter=100, alpha=0.1, verbose=False,
                 early_stopping=True, hidden_layer_sizes=(100, 10)),
    KNeighborsRegressor(n_neighbors=5),
    SVR(),
    SGDRegressor(penalty='l1', max_iter=50, alpha=0.001,
                 early_stopping=True, n_iter_no_change=3),
]

cls_estimators = [
    LogisticRegression(max_iter=100, penalty='l2', C=1, solver='saga'),
    RandomForestClassifier(n_estimators=100, max_depth=5, criterion='entropy'),
    GradientBoostingClassifier(n_estimators=100, loss='deviance'),
    XGBClassifier(n_estimators=100, eval_metric='merror'),
    LGBMClassifier(n_estimators=100, is_unbalance=True),
    ExtraTreesClassifier(n_estimators=100, criterion='entropy'),
    HistGradientBoostingClassifier(),
    MLPClassifier(max_iter=100, alpha=0.1, verbose=False,
                  early_stopping=True, hidden_layer_sizes=(100, 10)),
    KNeighborsClassifier(n_neighbors=5),
    SVC(gamma='auto'),
    SVC(kernel="linear", C=0.025),
    DecisionTreeClassifier(max_depth=5, criterion='entropy'),
    AdaBoostClassifier(),
    QuadraticDiscriminantAnalysis(),
    GaussianNB(),
]

def model_search(X, y, estimator, **kargs):
    params = init_params({'func': 'model_search', 'by': 'fit_Time', 'nmodel':7, 'cv':10, 'title': f'{estimator} Model Search'}, **kargs)
    
    if params['nmodel'] > 0:
        models = cls_estimators[:params['nmodel']] if estimator == 'cls' else reg_estimators[:params['nmodel']]
    else:
        models = cls_estimators if estimator == 'cls' else reg_estimators
        
        
    results  = []
    for i, model in enumerate(models):
        if params['verbose']:
            print(f'({i+1}/{len(models)}) {estimator}_model_test: {model.__class__.__name__}\n{model.get_params()}')
        else:
            print(f'({i+1}/{len(models)}) {estimator}_model_test: {model.__class__.__name__}')
        results.append(cv_score(model, X, y, estimator, params['cv'], model.__class__.__name__))
    rtn = pd.concat(results, axis=1).T
    if params['sort']:
        rtn = rtn.sort_values(params['by'], ascending=params['ascending'])
    if params['plot']:
        rtn.plot.bar(figsize=params['figsize'], cmap=params['cmap'],
                     width=params['width'], alpha=params['alpha'])
        plt.xticks(rotation=params['rotation'])
        plt.title(params['title'])
        plt.show()
    return rtn


#########################################################################################################
# 모델 검증
#########################################################################################################

from sklearn.model_selection import cross_validate
def cv_score(model, X, y, estimator, cv=10, title=None):
    return cv_cls_score(model, X, y, cv, title) if estimator == 'cls' else cv_reg_score(model, X, y, cv, title)


def cv_reg_score(model, X, y, cv=10, title=None, verbose=False):
    cv = cross_validate(model, X, y, cv=cv, scoring=(
        'neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'), return_train_score=True)
    if title == None:
        title = model.__class__.__name__
    tmp = pd.DataFrame(cv).mean()
    data = {'fit_Time': tmp['fit_time'], 'train_MAE': -tmp['train_neg_mean_absolute_error'], 'train_RMSE': -tmp['train_neg_root_mean_squared_error'],
            'train_R2': tmp['train_r2'], 'test_MAE': -tmp['test_neg_mean_absolute_error'], 'test_RMSE': -tmp['test_neg_root_mean_squared_error'], 'test_R2': tmp['test_r2']}
    if verbose:
        print(cv)
    return pd.DataFrame(data=data, index=[title]).T

cv_bi_score = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
cv_mt_score = ['accuracy', 'precision_macro', 'recall_macro',
                'f1_macro', 'precision_micro', 'recall_micro', 'f1_micro', 'roc_auc_ovo']

def cv_cls_score(model, X, y, cv=10, title=None, verbose=False):
    scoring = cv_mt_score if len(np.unique(y)) > 2 else cv_bi_score
    cv = cross_validate(model, X, y, cv=cv, scoring=scoring,
                        return_train_score=True)
    tmp = pd.DataFrame(cv).mean()
    if title == None:
        title = model.__class__.__name__
    if len(np.unique(y)) > 2:
        data = {'fit_Time': tmp['fit_time'], 'train_accuracy': tmp['train_accuracy'], 'train_precision_macro': tmp['train_precision_macro'],
                'train_recall_macro': tmp['train_recall_macro'], 'train_f1_macro': tmp['train_f1_macro'], 'train_precision_micro': tmp['train_precision_micro'],
                'train_recall_micro': tmp['train_recall_micro'], 'train_f1_micro': tmp['train_f1_micro'], 'train_roc_auc_ovo': tmp['train_roc_auc_ovo'], 'test_accuracy': tmp['test_accuracy'],
                'test_precision_macro': tmp['test_precision_macro'], 'test_recall_macro': tmp['test_recall_macro'], 'test_f1_macro': tmp['test_f1_macro'],
                'test_precision_micro': tmp['test_precision_micro'], 'test_recall_micro': tmp['test_recall_micro'], 'test_f1_micro': tmp['test_f1_micro'], test_roc_auc_ovo: tmp['test_roc_auc_ovo']}
    else:
        data = {'fit_Time': tmp['fit_time'], 'train_accuracy': tmp['train_accuracy'], 'train_precision': tmp['train_precision'],
                'train_recall': tmp['train_recall'], 'train_f1': tmp['train_f1'], 'train_roc_auc': tmp['train_roc_auc'], 'test_accuracy': tmp['test_accuracy'],
                'test_precision': tmp['test_precision'], 'test_recall': tmp['test_recall'], 'test_f1': tmp['test_f1'], 'test_roc_auc': tmp['test_roc_auc']}
    if verbose:
        print(cv)
    return pd.DataFrame(data=data, index=[title]).T




#########################################################################################################
# 기타
#########################################################################################################
from sklearn.cluster import KMeans


def plt_scree(estimator, X, **kargs):
    params = init_params({'max_comp':10, 'title':'Scree Plot'}, **kargs)

    plt.figure(plt.figure(figsize=params['figsize']))
    if estimator == 'kmeans':
        x = range(1, params['max_comp'])
        wss = []
        for i in x:
            kmeans = KMeans(n_clusters=i)
            kmeans.fit(X)
            wss.append(kmeans.inertia_)
        plt.plot(x, wss, marker=markers[0])
        xlabel, ylabel = 'Number of k value', 'WSS'
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(params['title'])
    plt.show()
    


#########################################################################################################
# 회귀분석 - reg
#########################################################################################################
def reg_equation(model, columns, name='model', round=3):
    equa = list(model.coef_)
    equa.insert(0, model.intercept_)
    cols = columns.insert(0, 'intercept')
    return pd.DataFrame(data=equa, columns=[name], index=cols)

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def reg_poly_fit(X, y, degree, plot=False, figsize=(12,5)):
    xval = np.linspace(np.min(X), np.max(X), 100).reshape(-1, 1)
    yval = {}
    for n in range(1, degree+1):
        model = make_pipeline(
            PolynomialFeatures(degree=n),
            LinearRegression(fit_intercept=True)
        ).fit(X, y)
        yval['poly'+str(n)] = np.ravel(model.predict(xval))
    rtn = pd.DataFrame(data=yval, index=np.ravel(xval))
    rtn.index.name = 'X'
    if plot:
        plt.figure(figsize=figsize)
        plt.scatter(X, y, c='k', alpha=0.2, label='data')
        for i, c in enumerate(rtn.columns):
                plt.plot(rtn.index, rtn[c], color=colors[i], lw=3, alpha=.7, label=c)
        plt.title(f'Reg Plot(Degree 1 ~ {degree})')
        plt.xlabel('Features')
        plt.ylabel('Target')
        plt.legend()
        plt.show()
    return rtn

def reg_poly_resid(X, y, degree, scoring='se', plot=False, figsize=(12,5)):
    models = []
    xval = X
    yval = {}
    for n in range(1, degree+1):
        model = make_pipeline(
            StandardScaler(),
            PolynomialFeatures(degree=n),
            LinearRegression(fit_intercept=True)
        ).fit(X, y)
        models.append(model)
        if scoring == 'ae':
            yval['poly'+str(n)] = np.abs(np.ravel(model.predict(xval) - y))
        elif scoring == 'se':
            yval['poly'+str(n)] = np.square(np.ravel(model.predict(xval) - y))
        else:
            yval['poly'+str(n)] = np.ravel(model.predict(xval) - y)
    rtn = pd.DataFrame(data=yval, index=np.ravel(xval)).sort_index(ascending=True)    
    rtn.index.name = 'X'
    if plot:
        plt.figure(figsize=figsize)
        color = sns.color_palette(palette)
        for i, c in enumerate(rtn.columns):
            plt.bar(rtn.index, rtn[c]+(i*0.2), color=color[i], alpha=0.5, label=c, width=0.3)
        plt.title(f'Reg Error(Degree 1 ~ {degree})')
        plt.xlabel('Features')
        plt.ylabel('Residuals')
        plt.legend()
        plt.show()
    return rtn



#########################################################################################################
# 모형 시각화 - show
#########################################################################################################
def show_feature_importance(model, columns, sort=False, plot=False, figsize=(12, 5)):
    rtn = pd.DataFrame(data=np.array(model.feature_importances_), index=columns, columns=['importances'])
    if sort:
        rtn = rtn.sort_values(by='importances', ascending=False)
    if plot:
        rtn.plot.bar(figsize=figsize, cmap=plt.cm.Set1)
        plt.show()
    return rtn

def show_decision_boundaries(X, y, decision_model, **model_params):
    '''
    input :  X : dataframe(over 2 Features, 2개 이상이면 앞쪽 2개 변수만 사용)
             y : target
    '''
    features = X.columns

    X = np.array(X)
    y = np.array(y).flatten()
    reduced_data = X[:, :2]
    model = decision_model(**model_params).fit(reduced_data, y)
    h = .02
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])    
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.Set1)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=15, alpha=0.5, cmap=plt.cm.Set1)
    plt.xlabel(features[0])
    plt.ylabel(features[0])
    return plt


#########################################################################################################
# 모형 평가 - show
#########################################################################################################
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def metric_reg_score(y_test, y_pred, title='model'):
    rtn = pd.DataFrame(
        data = [
            np.round(mean_absolute_error(y_test, y_pred), 3),
            np.round(mean_squared_error(y_test, y_pred), 3),
            np.round(np.sqrt(mean_squared_error(y_test, y_pred)), 3),
            np.round(r2_score(y_test, y_pred), 3)
            ],
        columns = [title],
        index=['mae', 'mse', 'rmse', 'r2']
    )
    return rtn

from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score)


def metric_cls_score(y_test, y_pred, title='model'):
    scoring = cv_mt_score if y.nunique() > 2 else cv_bi_score
    if y_test.nunique() > 2:
        rtn = pd.DataFrame(data=[
            accuracy_score(y_test, y_pred),
            precision_score(y_test, y_pred, average='macro'),
            recall_score(y_test, y_pred, average='macro'),
            f1_score(y_test, y_pred, average='macro'),
            precision_score(y_test, y_pred, average='micro'),
            recall_score(y_test, y_pred, average='micro'),
            f1_score(y_test, y_pred, average='micro')],
        columns=[title],
        index = scoring)
    else:
        rtn = pd.DataFrame(data=[
            accuracy_score(y_test, y_pred),
            precision_score(y_test, y_pred),
            recall_score(y_test, y_pred),
            f1_score(y_test, y_pred)],
        columns=[title],
        index = scoring)
    return rtn

from sklearn.metrics import plot_roc_curve, roc_auc_score


def metric_cls_auc_score(model, X_test, y_test, round=3, plot=True, figsize=(12,5)):
    if y_test.nunique() > 2:
        auc_score = roc_auc_score(y_test, model.predict_proba(X_test), multi_class='ovr')
    else:
        auc_score = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
        if plot:
            fig, ax = plt.subplots(figsize=figsize)
            plot_roc_curve(model, X_test, y_test, ax=ax)
            plt.show()
    return np.round(auc_score, round)
