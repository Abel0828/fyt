# created by you xiu de bang bang :P

df=pd.read_csv('../data/Jinshenlu2.txt',sep='\t',
              error_bad_lines=False, low_memory=False,
              usecols=['xuhao', 'year', 'diqu', 'jigou_1', 'jigou_2', 'jigou_3',
                       'core_guanzhi', 'pinji_detailed', 'pinji_numeric', 'unique_id', 'fangkeben_only', 'qiren'])
df.dropna(subset=['unique_id'], inplace=True) # drop unusable entries that don't have unique_id
df=df[(df['xuhao']<20000) & (df['qiren']=='民人') & (df['fangkeben_only']<0.5)] # apply filteration

# the following snippet tries best to recover around 2% of the data in pinji_detailed
dic=dict(zip(['一', '二','三','四','五', '六','七','八','九'], np.arange(1,10)))
guanzhi_pj=df[['core_guanzhi','pinji_detailed']].copy(deep=True).set_index('core_guanzhi').to_dict('index') #convert to dict for quick lookup
def str2float(x):
    s=x[0]
    if pd.isnull(s):
        n=x[1]
        gz=x[2]
        global guanzhi_pj
        pj=guanzhi_pj.get(gz)
        found=False
        if pj:
            if pd.notnull(pj['pinji_detailed']):
                s=pj['pinji_detailed']
                found=True
        if not found:
            if n:
                if n==0.0:
                    return 10.0
                return n
            else:
                return np.nan
    if s in ['不入流', '未入流']:
        return 10.0
    if s=='從一品(應為正四品)':
        return 4.0
    if s=='從物品':
        return 5.5
    if s=='鄭路平':
        return 6.0
    global dic
    base = dic[s[-2]]
    base+=0.5*('從' in s)
    return float(base)
df['pinji_detailed_numeric']=df[['pinji_detailed', 'pinji_numeric', 'core_guanzhi']].apply(str2float, axis=1)
df.drop(['xuhao', 'pinji_detailed', 'pinji_numeric', 'fangkeben_only', 'qiren'], axis=1, inplace=True)
df.dropna(subset=['pinji_detailed_numeric'], inplace=True)
df.describe(include='all')