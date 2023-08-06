import pandas
import pickle
from tqdm import tqdm
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydatamail.database import DatabaseTemplate


Base = declarative_base()


class MachineLearningLabels(Base):
    __tablename__ = "ml_labels"
    id = Column(Integer, primary_key=True)
    label_id = Column(String)
    random_forest = Column(String)
    user_id = Column(Integer)


class MachineLearningDatabase(DatabaseTemplate):
    def store_models(self, model_dict, user_id=1, commit=True):
        label_lst = self._get_labels(user_id=user_id)
        model_dict_new = {k: v for k, v in model_dict.items() if k not in label_lst}
        model_dict_update = {k: v for k, v in model_dict.items() if k in label_lst}
        model_delete_lst = [
            label for label in label_lst if label not in model_dict.keys()
        ]
        if len(model_dict_new) > 0:
            self._session.add_all(
                [
                    MachineLearningLabels(
                        label_id=k, random_forest=pickle.dumps(v), user_id=user_id
                    )
                    for k, v in model_dict_new.items()
                ]
            )
        if len(model_dict_update) > 0:
            label_obj_lst = (
                self._session.query(MachineLearningLabels)
                .filter(MachineLearningLabels.user_id == user_id)
                .filter(
                    MachineLearningLabels.label_id.in_(list(model_dict_update.keys()))
                )
                .all()
            )
            for label_obj in label_obj_lst:
                label_obj.random_forest = pickle.dumps(
                    model_dict_update[label_obj.label_id]
                )
        if len(model_delete_lst) > 0:
            self._session.query(MachineLearningLabels).filter(
                MachineLearningLabels.user_id == user_id
            ).filter(MachineLearningLabels.label_id.in_(model_delete_lst)).delete()
        if commit:
            self._session.commit()

    def load_models(self, user_id=1):
        label_obj_lst = (
            self._session.query(MachineLearningLabels)
            .filter(MachineLearningLabels.user_id == user_id)
            .all()
        )
        return {
            label_obj.label_id: pickle.loads(label_obj.random_forest)
            for label_obj in label_obj_lst
        }

    def train_model(
        self, df, labels_to_learn=None, user_id=1, n_estimators=10, random_state=42
    ):
        if labels_to_learn is None:
            labels_to_learn = [c for c in df.columns.values if "labels_Label_" in c]
        df_in = get_training_input(df=df).sort_index(axis=1)
        model_dict = {
            to_learn.split("labels_")[-1]: self._train_randomforest(
                df_in=df_in,
                results=df[to_learn],
                n_estimators=n_estimators,
                random_state=random_state,
            )
            for to_learn in tqdm(labels_to_learn)
        }
        self.store_models(model_dict=model_dict, user_id=user_id)
        return model_dict

    def get_models(
        self, df, user_id=1, n_estimators=10, random_state=42, recalculate=False
    ):
        labels_to_learn = [c for c in df.columns.values if "labels_Label_" in c]
        label_name_lst = [to_learn.split("labels_")[-1] for to_learn in labels_to_learn]
        if not recalculate and sorted(label_name_lst) == sorted(
            self._get_labels(user_id=user_id)
        ):
            return self.load_models(user_id=user_id)
        else:
            return self.train_model(
                df=df,
                labels_to_learn=labels_to_learn,
                user_id=user_id,
                n_estimators=n_estimators,
                random_state=random_state,
            )

    def _get_labels(self, user_id=1):
        return [
            label[0]
            for label in self._session.query(MachineLearningLabels.label_id)
            .filter(MachineLearningLabels.user_id == user_id)
            .all()
        ]

    @staticmethod
    def _train_randomforest(df_in, results, n_estimators=1000, random_state=42):
        return RandomForestRegressor(
            n_estimators=n_estimators, random_state=random_state
        ).fit(df_in, results)


def _build_red_lst(df_column):
    collect_lst = []
    for lst in df_column:
        for entry in lst:
            collect_lst.append(entry)
    return list(set(collect_lst))


def _single_entry_df(df, red_lst, column):
    return [
        {
            column + "_" + red_entry: 1 if email == red_entry else 0
            for red_entry in red_lst
            if red_entry is not None
        }
        for email in df[column].values
    ]


def _list_entry_df(df, red_lst, column):
    return [
        {
            column + "_" + red_entry: 1 if red_entry in email else 0
            for red_entry in red_lst
        }
        for email in df[column].values
    ]


def _merge_dicts(
    email_id, label_dict, cc_dict, from_dict, threads_dict, to_dict, label_lst
):
    email_dict_prep = {"email_id": email_id}
    email_dict_prep.update(label_dict)
    email_dict_prep.update(cc_dict)
    email_dict_prep.update(from_dict)
    email_dict_prep.update(threads_dict)
    email_dict_prep.update(to_dict)
    if len(label_lst) == 0:
        return email_dict_prep
    else:
        email_dict = {k: v for k, v in email_dict_prep.items() if k in label_lst}
        email_dict.update(
            {label: 0 for label in label_lst if label not in email_dict.keys()}
        )
        return email_dict


def one_hot_encoding(df, label_lst=[]):
    dict_labels_lst = _list_entry_df(
        df=df, red_lst=_build_red_lst(df_column=df.labels.values), column="labels"
    )
    dict_cc_lst = _list_entry_df(
        df=df, red_lst=_build_red_lst(df_column=df.cc.values), column="cc"
    )
    dict_from_lst = _single_entry_df(df=df, red_lst=df["from"].unique(), column="from")
    dict_threads_lst = _single_entry_df(
        df=df, red_lst=df["threads"].unique(), column="threads"
    )
    dict_to_lst = _list_entry_df(
        df=df, red_lst=_build_red_lst(df_column=df.to.values), column="to"
    )
    return pandas.DataFrame(
        [
            _merge_dicts(
                email_id=email_id,
                label_dict=label_dict,
                cc_dict=cc_dict,
                from_dict=from_dict,
                threads_dict=threads_dict,
                to_dict=to_dict,
                label_lst=label_lst,
            )
            for email_id, label_dict, cc_dict, from_dict, threads_dict, to_dict in zip(
                df.id.values,
                dict_labels_lst,
                dict_cc_lst,
                dict_from_lst,
                dict_threads_lst,
                dict_to_lst,
            )
        ]
    )


def get_training_input(df):
    return df.drop(
        [c for c in df.columns.values if "labels_" in c] + ["email_id"], axis=1
    )


def get_machine_learning_database(engine, session):
    Base.metadata.create_all(engine)
    return MachineLearningDatabase(session=session)
