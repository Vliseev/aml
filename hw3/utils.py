import gc
import pickle
from dataclasses import dataclass
from typing import Any, List

import numpy as np
from scipy.sparse import coo_matrix, hstack
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import OneHotEncoder


@dataclass
class CommandResult:
    players: List[int]
    mask: str


@dataclass
class TourData:
    tour_id: int
    num_questions: int
    results: List[CommandResult]


def get_id_by_years(y, t_dict):
    ids = []
    for id_val in t_dict:
        if t_dict[id_val]['dateStart'].startswith(y):
            ids.append(id_val)
    return ids


def get_player_ids(index, result_df):
    player_idx = []
    for idx in index:
        results = result_df[idx]
        for result in results:
            for player in result['teamMembers']:
                player_idx.append(player['player']['id'])
    return player_idx


def get_data(indexes, result_data, tournament):
    data = []
    for idx in indexes:
        result_query = []
        for result in result_data[idx]:
            pl_id = [player['player']['id']
                     for player in result['teamMembers']]
            if 'mask' in result:
                mask = result['mask']
                result_query.append(CommandResult(pl_id, mask))
        total_cuestion = sum(tournament[idx]['questionQty'].values())
        data.append(TourData(idx, total_cuestion, result_query))
    return data


def get_train_data_tour(tour_data: TourData, total_question, quest_offset):
    X = [list() for _ in range(2)]
    y = []
    for result in tour_data.results:
        if result.mask is None:
            continue
        questions = [int(s) for s in result.mask if s in ('0', '1')]
        num_question = len(questions)
        if num_question != total_question:
            continue
        for player in result.players:
            X_player = [player] * num_question
            question_id = []
            X[0].extend(X_player)
            X[1].extend(type_quest)
            y.extend(questions)
    X = np.array(X).T
    y = np.array(y)
    return X, y


def get_test_data_comm(result: CommandResult, quest_id, train_players):
    X = [list() for _ in range(2)]
    y = []

    if result.mask:
        questions = [int(s) for s in result.mask if s in ('0', '1')]
        num_question = len(questions)
        for player in result.players:
            if player in train_players:
                X_player = [player] * num_question
                type_quest = [quest_id] * num_question
                X[0].extend(X_player)
                X[1].extend(type_quest)
                y.extend(questions)
    X = np.array(X).T
    y = np.array(y)
    return X, y


def get_train_data(train_data):
    X, y = [], []
    for t in train_data:
        X_new, y_new = get_train_data_tour(t)
        X.append(X_new)
        y.extend(y_new)
    X = np.vstack(X)
    y = np.array(y)
    return X, y


def main():
    pass


if __name__ == '__main__':
    main()
