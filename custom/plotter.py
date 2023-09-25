from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import os 
import glob

def plotter(log_path:str,img_path:str):
    count = 0
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    for file in glob.glob(log_path+'/*'):
        for file_sub in glob.glob(file+'/*'):
            if file_sub.split('.')[-1]=='csv':
                df = pd.read_csv(file_sub)
                count+=1
                if count ==1:
                    df_old = df.copy()
                else:
                    df_old = pd.concat([df_old,df],axis=0,ignore_index=True)
    df_old = df_old.reset_index() 
    #first image

    fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("reward", "Min", "Episode Length" ,"Max"))
    fig.add_trace(go.Scatter(name='reward',x=df_old.index.to_numpy(),y= df_old.episode_reward_mean.to_numpy(),),
                row=1, col=1)
    fig.add_trace(go.Scatter(name='min',x=df_old.index.to_numpy(), y=df_old.episode_reward_min.to_numpy()),
                row=1, col=2)

    fig.add_trace(go.Scatter(name='max',x=df_old.index.to_numpy(),y= df_old.episode_reward_max.to_numpy()),
                row=2, col=2)
    fig.add_trace(go.Scatter(name='len',x=df_old.index.to_numpy(),y= df_old.episode_len_mean.to_numpy()),
                row=2, col=1)
    fig.update_layout(
        autosize=False,
        width=1200,
        height=700,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=1
        ),showlegend=False
        # paper_bgcolor="Black",
    )
    fig.update_xaxes(title_text='train iters')
    fig.write_image(f"{img_path}/fig1.png")
    #second image
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("gradient norm","Current kl coefficient",  "Number of agent steps trained","mean y distance both agents"))
    fig.add_trace(go.Scatter(name='grad_gnorm',x=df_old.index.to_numpy(),y= df_old['info/learner/default_policy/learner_stats/grad_gnorm'].to_numpy(),),
                row=1, col=1)
    fig.add_trace(go.Scatter(name='curr_kl_coeff',x=df_old.index.to_numpy(), y=df_old['info/learner/default_policy/learner_stats/cur_kl_coeff'].to_numpy()),
                row=1, col=2)

    fig.add_trace(go.Scatter(name='mean_dist',x=df_old.index.to_numpy(),y= df_old['custom_metrics/y_direction_mean_both_agents'].to_numpy()),
                row=2, col=2)
    fig.add_trace(go.Scatter(name='agent steps trained',x=df_old.index.to_numpy(),y= df_old['num_agent_steps_trained'].to_numpy()),
                row=2, col=1)
    fig.update_layout(
        autosize=False,
        width=1200,
        height=700,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=1
        ),showlegend=False
        # paper_bgcolor="Black",
    )
    fig.update_xaxes(title_text='train iters')
    fig.write_image(f"{img_path}/fig2.png")


    #third image

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("entropy","Maximum y distance both agents",  "Value Function Explained Variance","KL"))
    fig.add_trace(go.Scatter(name='entropy',x=df_old.index.to_numpy(),y= df_old['info/learner/default_policy/learner_stats/entropy'].to_numpy(),),
                row=1, col=1)
    fig.add_trace(go.Scatter(name='max_both',x=df_old.index.to_numpy(), y=df_old['custom_metrics/y_direction_max_both_agents'].to_numpy()),
                row=1, col=2)

    fig.update_layout(
        autosize=False,
        width=1200,
        height=350,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=1
        ),showlegend=False
        # paper_bgcolor="Black",
    )
    fig.update_xaxes(title_text='train iters')
    fig.write_image(f"{img_path}/fig3.png")


    #fifth image

    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("total Loss","Policy Loss",  "Value Function Explained Variance","KL"))
    fig.add_trace(go.Scatter(name='total_loss',x=df_old.index.to_numpy(),y= df_old['info/learner/default_policy/learner_stats/total_loss'].to_numpy(),),
                row=1, col=1)
    fig.add_trace(go.Scatter(name='policy_loss',x=df_old.index.to_numpy(), y=df_old['info/learner/default_policy/learner_stats/policy_loss'].to_numpy()),
                row=1, col=2)

    fig.add_trace(go.Scatter(name='kl',x=df_old.index.to_numpy(),y= df_old['info/learner/default_policy/learner_stats/kl'].to_numpy()),
                row=2, col=2)
    fig.add_trace(go.Scatter(name='vf_explained_var',x=df_old.index.to_numpy(),y= df_old['info/learner/default_policy/learner_stats/vf_explained_var'].to_numpy()),
                row=2, col=1)
    fig.update_layout(
        autosize=False,
        width=1200,
        height=700,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=1
        ),showlegend=False
        # paper_bgcolor="Black",
    )
    fig.update_xaxes(title_text='train iters')
    fig.write_image(f"{img_path}/fig4.png")
    