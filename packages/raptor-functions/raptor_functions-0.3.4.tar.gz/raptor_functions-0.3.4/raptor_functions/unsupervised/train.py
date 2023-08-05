

from raptor_functions.supervised.feature_extraction import  *
# from raptor_functions.unsupervised.train import *
# from raptor_functions.supervised.preprocess import  *
import optuna
import mlflow
import os

# try:
#     from sklearn.utils import safe_indexing
# except ImportError:
#     from sklearn.utils import _safe_indexing

from pathlib import Path
from mlflow.models.signature import infer_signature
from pycaret.clustering import *

# df = get_data('handheld_data')

# def get_clusters(df, model_name='kmeans', num_clusters=2):
#     unique_id = 'exp_unique_id'
#     label = 'result'

#     y = df.groupby(unique_id).first()[label]
#     X = df.drop(label, axis=1)

#     X = get_all_features(X)
#     df_extracted = X.join(y)

#     # df_f = get_training_features(df)


#     cluster = setup(X, session_id = 7652)

#     model = create_model(model_name, num_clusters)

#     # plot_model(model, 'elbow')
#     plot_model(model, 'cluster')


#     results = assign_model(model)
#     return results, model





# Importing the Packages:
import optuna
import mlflow
import os

# try:
#     from sklearn.utils import safe_indexing
# except ImportError:
#     from sklearn.utils import _safe_indexing

from pathlib import Path
from mlflow.models.signature import infer_signature
from explainerdashboard import ExplainerDashboard, ClassifierExplainer

SENSORS_FEATURES = [
    "sensor_1",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_5",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_10",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_16",
    "sensor_17",
    "sensor_18",
    "sensor_19",
    "sensor_20",
    "sensor_21",
    "sensor_22",
    "sensor_23",
    "sensor_24",
]

STAGES = ["baseline", "absorb", "pause", "desorb", "flush"]
TARGET_COL = "result"
REMOTE_TRACKING_URI = "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"


# 'http://ec2-3-10-210-150.eu-west-2.compute.amazonaws.com:5000/'


def get_plots(model):

    model_attributes = dir(model)

    plot_dir = os.path.join(os.getcwd(), "plots")
    Path(plot_dir).mkdir(parents=True, exist_ok=True)

    # plot_model(model, plot="confusion_matrix", save=plot_dir)
    # cm = os.path.join(plot_dir, "Confusion Matrix.png")
    # mlflow.log_artifact(cm)
    # log_artifact(cm)

    try:
        plot_model(model, 'elbow', save=plot_dir)
    except:
        pass

    try:
        plot_model(model, 'cluster', save=plot_dir)
    except:
        pass

    try:
        plot_model(model, 'tsne', save=plot_dir)
    except:
        pass

    try:
        plot_model(model, 'silhoutte', save=plot_dir)
    except:
        pass

    try:
        plot_model(model, 'distance', save=plot_dir)
    except:
        pass

    try:
        plot_model(model, 'distribution', save=plot_dir)
    except:
        pass

    
    
    
    
    

    
    mlflow.log_artifact(plot_dir)





def objective(trial, X, study_name, model_mode):



    mlflow.set_experiment(study_name)

    mlflow.set_tracking_uri(REMOTE_TRACKING_URI)


    unique_id = 'exp_unique_id'
    label = 'result'
    num_clusters = 2
    model_name='kmeans'

    # y = df.groupby(unique_id).first()[label]
    # X = df.drop(label, axis=1)

    # X = get_all_features(X)
    # df_extracted = X.join(y)

    # df_f = get_training_features(df)






    # results = assign_model(model)

    # df_offset = df.filter(regex='offset')
    # df_gradient = df.filter(regex='gradient')

    # if len(df_offset.columns) > 0:
    #     offset = True
    # else:
    #     offset = False

    # if len(df_gradient.columns) > 0:
    #     gradient = True
    # else:
    #     gradient = False
    

    # df_copy = df.copy(deep=True)

    # relevant_features = list(df_copy.drop(TARGET_COL, axis=1).columns)

    mlflow.start_run()

    # # remove unwanted characters from the column names
    # df_copy.columns = df_copy.columns.str.replace('["]', "")

    # features = df_copy.drop(TARGET_COL, axis=1)

    # df_copy["result"] = df_copy["result"].replace({"Control": 0, "Covid": 1})

    features = X
    relevant_features = list(X.columns)


    cluster = setup(X)

    MODELS = dict(models()["Name"])



    model_id = trial.suggest_categorical("model", list(MODELS.keys()))
    model_name = MODELS[model_id]
    model = create_model(model_id, num_clusters)
    
    # model = create_model(model_name, num_clusters)

    results = assign_model(model)




    MODELS = dict(models()["Name"])

    get_plots(model)

    metrics = get_metrics()
    # print(metrics)
    # mlflow.log_metrics(metrics)


    try:
        signature = infer_signature(features, predict_model(model, data=features))
        mlflow.sklearn.log_model(model, artifact_path=model_name, signature=signature)

    except:
        pass


    model_params = model.get_params()



        
    

    




    # mlflow.log_metrics(metrics)

    try:
        # mlflow.set_tag('features', features)
        mlflow.set_tag("relevant_features", relevant_features)

    except:
        pass

    mlflow.set_tag("model_name", model_name)
    # mlflow.set_tag("offset", offset)
    # mlflow.set_tag("gradient", gradient)
    mlflow.set_tag("model_params", model_params)


    mlflow.set_tag("model_mode", model_mode)

    mlflow.end_run()


def train_experiments(
    df, study_name="unsupervised", direction="maximize", model_mode="random", n_trials=5
):
    """trains several models during different trials and logs them. Experiemnt can be tracked on "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"


    Args:
        df (pandas dataframe): dataframe of cyclic sensor data to be used for training
        study_name (str, optional): optuna study name to use. Defaults to 'unsupervised'.
        direction (str, optional): direction of objective. Defaults to 'maximize'.
        model_mode (str, optional): _description_. Defaults to 'random'.
        n_trials (int, optional): number of times to run experiments. Defaults to 5.
    """

    study = optuna.create_study(study_name=study_name, direction=direction)
    study.optimize(
        lambda trial: objective(trial, df, study_name, model_mode), n_trials=n_trials
    )

    print("Click on this link to track experiments: ", REMOTE_TRACKING_URI)
































# def plot_new_sample(df, x):

#     X = df.iloc[:, 1:13]
#     y = df["label"].replace({"Control": 0, "Covid": 1})  # .value_counts()
#     x = x.values.reshape(1, -1)

#     scaler = StandardScaler()
#     scaler.fit(X.values)
#     X = scaler.transform(X.values)

#     means = np.array(
#         [
#             243.94969928,
#             256.31424094,
#             313.33404167,
#             311.02738043,
#             284.31009239,
#             307.20553442,
#             293.71868478,
#             298.39285688,
#             276.90539674,
#             303.74205978,
#             262.39199638,
#             228.63297464,
#         ]
#     )
#     vars = np.array(
#         [
#             32.38231873,
#             15.39840351,
#             0.30922943,
#             0.11581567,
#             14.18706441,
#             0.67305964,
#             2.09758948,
#             0.96071839,
#             7.81709395,
#             1.53088058,
#             4.84237249,
#             13.75799395,
#         ]
#     )

#     # means = scaler.mean_
#     # vars = scaler.var_

#     print("mean: ", means)
#     print("var: ", vars)

#     # X = scale_data(X.values, means=means,stds=vars **0.5)
#     x = scale_data(x, means=means, stds=vars ** 0.5)

#     print("scaled_new_data: ", x)

#     pca = PCA(n_components=2)
#     X = pca.fit_transform(X)

#     # # print('Scaled X: ', X)

#     print("before pca: ", x)
#     x = pca.transform(x)
#     print("after pca: ", x)

#     # x = scaler.transform(x)
#     # print(x)

#     # pipe = Pipeline([
#     #     ('scale', StandardScaler()),
#     #     ('reduce_dims', PCA(n_components=2))])

#     # pipe.fit(X.values)
#     # X = pipe.transform(X.values)

#     # print('pca_comp: ', x)

#     group = y
#     # group = y[:-10]
#     cdict = {0: "blue", 1: "red"}
#     class_label = {0: "Control", 1: "Covid"}

#     scatter_x = X[:, 0]
#     scatter_y = X[:, 1]

#     fig, ax = plt.subplots()
#     for g in np.unique(group):
#         ix = np.where(group == g)
#         ax.scatter(
#             scatter_x[ix], scatter_y[ix], c=cdict[g], label=class_label[g], alpha=0.5
#         )
#     ax.scatter(x[:, 0], x[:, 1], c="black", label="new sample", s=70)
#     ax.legend()
#     ax.set_title("New data cluster assignment")
#     ax.set_xlabel("PC1")
#     ax.set_ylabel("PC2")
#     # plt.show()
#     fig.savefig("./static/img/sample_cluster.jpeg")
