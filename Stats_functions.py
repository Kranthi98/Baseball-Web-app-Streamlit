
@st.cache()
def stats_by_pitchtypes(df):
    master_cols = ['None', 'caught_stealing_2b', 'double', 'field_error', 'field_out',
       'fielders_choice', 'fielders_choice_out', 'force_out',
       'grounded_into_double_play', 'hit_by_pitch', 'home_run', 'intent_walk',
       'sac_bunt', 'sac_fly', 'single', 'strikeout', 'strikeout_double_play',
       'triple', 'walk', 'fly_ball', 'ground_ball', 'line_drive', 'popup']

    bb_types = df.bb_type.dropna().unique()
    AB_cols = df.events.unique()
    Hit_cols = ["single","double","triple","home_run"]
    df1 = pd.concat([pd.get_dummies(df[col]) for col in ["events","bb_type"]], axis = 1)

    df1[[x for x in master_cols if x not in df1.columns]] = 0

    df1 = (df1.assign(pitch_type = df.pitch_type)
                .groupby("pitch_type").sum()
                .assign(PT_per = df.pitch_type.value_counts(normalize = True).multiply(100).round(2),
                        GB = lambda x : x.ground_ball.div(x[bb_types].sum(axis = 1)).multiply(100).round(0),
                        FB = lambda x : x.fly_ball.div(x[bb_types].sum(axis = 1)).multiply(100).round(0),
                        GBtoFB = lambda x : x.ground_ball.div(x.fly_ball),
                        AB = lambda x : x[AB_cols].sum(1),
                        Hits = lambda x : x[Hit_cols].sum(1),
                        BA = lambda x : x.Hits.div(x.AB).round(3),
                        TotalBases = lambda x : sum(x[y]*(i+1) for i, y in enumerate(("single","double","triple","home_run"))),
                        SLG = lambda x : x.TotalBases.div(x.AB).round(3),
                        OBP = lambda x : x.walk.add(x.Hits).div(x[["walk","Hits","sac_fly"]].sum(1)).round(3),
                        HR_per_AB = lambda x : x.home_run.div(x.AB).round(3),
                        HR_per_FB = lambda x : x.home_run.div(x.fly_ball).round(3),
                        ISO = lambda x : sum(x[y]*(i+1) for i,y in enumerate(("double","triple","home_run"))).div(x.AB).round(3),
                        BABIP = lambda x : x.Hits.sub(x.home_run).div(x.AB.sub(x[["strikeout","home_run","sac_fly"]].sum(1))).round(3),

                                        ))
    
    cols = ['PT_per',"BA","SLG","OBP","ISO","BABIP","GB","FB","GBtoFB","HR_per_AB","HR_per_FB",]
    return df1[cols].reset_index().round(2)




def remove_index():
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """
# Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
