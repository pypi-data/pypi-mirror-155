"""
Copyright 2021 Objectiv B.V.
"""
from typing import List, Union

import bach
from bach.series import Series
from sql_models.constants import NotSet, not_set
from typing import List, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from modelhub import ModelHub
    from modelhub.series import SeriesLocationStack

GroupByType = Union[List[Union[str, Series]], str, Series, NotSet]


class Aggregate:
    """
    Models that return aggregated data in some form from the original DataFrame with Objectiv data.
    """

    def __init__(self, mh: 'ModelHub'):
        self._mh = mh

    def _check_groupby(self,
                       data: bach.DataFrame,
                       groupby: Union[List[Union[str, Series]], str, Series],
                       not_allowed_in_groupby: str = None
                       ):

        if data.group_by:
            raise ValueError("can't run model hub models on a grouped DataFrame, please use parameters "
                             "(ie groupby of the model")

        groupby_list = groupby if isinstance(groupby, list) else [groupby]
        groupby_list = [] if groupby is None else groupby_list

        if not_allowed_in_groupby is not None and not_allowed_in_groupby not in data.data_columns:
            raise ValueError(f'{not_allowed_in_groupby} column is required for this model but it is not in '
                             f'the DataFrame')

        if not_allowed_in_groupby:
            for key in groupby_list:
                new_key = data[key] if isinstance(key, str) else key
                if new_key.equals(data[not_allowed_in_groupby]):
                    raise KeyError(f'"{not_allowed_in_groupby}" is in groupby but is needed for aggregation: '
                                   f'not allowed to group on that')

        grouped_data = data.groupby(groupby_list)
        return grouped_data

    def _generic_aggregation(self,
                             data: bach.DataFrame,
                             groupby: Union[List[Union[str, Series]], str, Series],
                             column: str,
                             name: str):

        self._mh._check_data_is_objectiv_data(data)

        data = self._check_groupby(data=data,
                                   groupby=groupby,
                                   not_allowed_in_groupby=column)

        series = data[column].nunique()
        return series.copy_override(name=name)

    def unique_users(self,
                     data: bach.DataFrame,
                     groupby: GroupByType = not_set) -> bach.SeriesInt64:
        """
        Calculate the unique users in the Objectiv ``data``.

        :param data: :py:class:`bach.DataFrame` to apply the method on.
        :param groupby: sets the column(s) to group by.

            - if not_set it defaults to using :py:attr:`ModelHub.time_agg`.
            - if None it aggregates over all data.
        :returns: series with results.
        """

        groupby = [self._mh.time_agg(data)] if groupby is not_set else groupby

        return self._generic_aggregation(data=data,
                                         groupby=groupby,
                                         column='user_id',
                                         name='unique_users')

    def unique_sessions(self,
                        data: bach.DataFrame,
                        groupby: GroupByType = not_set) -> bach.SeriesInt64:
        """
        Calculate the unique sessions in the Objectiv ``data``.

        :param data: :py:class:`bach.DataFrame` to apply the method on.
        :param groupby: sets the column(s) to group by.

            - if not_set it defaults to using :py:attr:`ModelHub.time_agg`.
            - if None it aggregates over all data.
        :returns: series with results.
        """

        groupby = [self._mh.time_agg(data)] if groupby is not_set else groupby

        return self._generic_aggregation(data=data,
                                         groupby=groupby,
                                         column='session_id',
                                         name='unique_sessions')

    def session_duration(self,
                         data: bach.DataFrame,
                         groupby: GroupByType = not_set,
                         exclude_bounces: bool = True,
                         method: 'str' = 'mean') -> bach.SeriesInt64:
        """
        Calculate the duration of sessions.

        With default `method`, it calculates the mean of the session duration over the `groupby`.

        :param data: :py:class:`bach.DataFrame` to apply the method on.
        :param groupby: sets the column(s) to group by.

            - if not_set it defaults to using :py:attr:`ModelHub.time_agg`.
            - if None it aggregates over all data.
        :param exclude_bounces: if True only session durations greater than 0 will be considered
        :param method: 'mean' or 'sum'
        :returns: series with results.
        """

        self._mh._check_data_is_objectiv_data(data)

        if groupby is not_set:
            groupby = self._mh.time_agg(data)

        if groupby is None:
            new_groupby = []
        elif not isinstance(groupby, list):
            new_groupby = [groupby]
        else:
            new_groupby = groupby
        new_groupby.append(data.session_id.copy_override(name='__session_id'))

        gdata = self._check_groupby(data=data, groupby=new_groupby)
        session_duration = gdata.aggregate({'moment': ['min', 'max']})
        session_duration['session_duration'] = session_duration['moment_max'] - session_duration['moment_min']

        if exclude_bounces:
            session_duration = session_duration[(session_duration['session_duration'].dt.total_seconds > 0)]

        if method not in ['sum', 'mean']:
            raise ValueError("only 'sum and 'mean' are supported for `method`")

        grouped_data = session_duration.groupby(session_duration.index_columns[:-1]).session_duration
        if method == 'sum':
            return grouped_data.sum()
        return grouped_data.mean()

    def frequency(self, data: bach.DataFrame) -> bach.SeriesInt64:
        """
        Calculate a frequency table for the number of users by number of sessions.

        :param data: :py:class:`bach.DataFrame` to apply the method on.
        :returns: series with results.
        """

        self._mh._check_data_is_objectiv_data(data)
        total_sessions_user = data.groupby(['user_id']).aggregate({'session_id': 'nunique'}).reset_index()
        frequency = total_sessions_user.groupby(['session_id_nunique']).aggregate({'user_id': 'nunique'})

        return frequency.user_id_nunique

    def top_product_features(self,
                             data: bach.DataFrame,
                             location_stack: 'SeriesLocationStack' = None,
                             event_type: str = 'InteractiveEvent') -> bach.DataFrame:
        """
        Calculate the top used features in the product.

        :param data: :py:class:`bach.DataFrame` to apply the method on.
        :param location_stack: the location stack

            - can be any slice of a :py:class:`modelhub.SeriesLocationStack` type column
            - if None - the whole location stack is taken.
        :param event_type: event type. Must be a valid event_type (either parent or child).
        :returns: bach DataFrame with results.
        """

        data = data.copy()

        self._mh._check_data_is_objectiv_data(data)

        # the following columns have to be in the data
        data['__application'] = data.global_contexts.gc.application

        if location_stack is not None:
            data['__feature_nice_name'] = location_stack.ls.nice_name
        else:
            data['__feature_nice_name'] = data.location_stack.ls.nice_name

        groupby_col = ['__application', '__feature_nice_name', 'event_type']

        # selects specific event types, so stack_event_types must be a superset of [event_types]
        interactive_events = data[data.stack_event_types.json.array_contains(event_type)]

        # users by feature
        users_feature = interactive_events.groupby(groupby_col).agg({'user_id': 'nunique'})

        # remove double underscores from the columns name
        columns = {
            col: col[2:] if col.startswith('__') else col
            for col in groupby_col
        }
        _index = list(columns.values())
        users_feature = users_feature.reset_index().rename(columns=columns)
        users_feature = users_feature.dropna().set_index(_index)

        return users_feature.sort_values('user_id_nunique', ascending=False)

    def top_product_features_before_conversion(self,
                                               data: bach.DataFrame,
                                               name: str,
                                               location_stack: 'SeriesLocationStack' = None,
                                               event_type: str = 'InteractiveEvent') -> bach.DataFrame:
        """
        Calculates what users did before converting by
        combining several models from the model hub.

        :param data: :py:class:`bach.DataFrame` to apply the method on.
        :param name: label of the conversion event.
        :param location_stack: the location stack

            - can be any slice of a :py:class:`modelhub.SeriesLocationStack` type column
            - if None - the whole location stack is taken.
        :param event_type: event type. Must be a valid event_type
            (either parent or child).
        :returns: bach DataFrame with results.
        """

        data = data.copy()
        self._mh._check_data_is_objectiv_data(data)

        if not name:
            raise ValueError('Conversion event label is not provided.')

        data['__application'] = data.global_contexts.gc.application

        if location_stack is not None:
            data['__feature_nice_name'] = location_stack.ls.nice_name
        else:
            data['__feature_nice_name'] = data.location_stack.ls.nice_name

        # label sessions with a conversion
        data['converted_users'] = self._mh.map.conversions_counter(data,
                                                                   name=name) >= 1

        # label hits where at that point in time, there are 0 conversions in the session
        data['zero_conversions_at_moment'] = self._mh.map.conversions_in_time(data,
                                                                              name) == 0

        # filter on above created labels
        converted_users = data[(data.converted_users & data.zero_conversions_at_moment)]

        # select only user interactions
        converted_users_filtered = converted_users[
            converted_users.stack_event_types.json.array_contains(event_type)
        ]

        groupby_col = ['__application', '__feature_nice_name', 'event_type']
        converted_users_features = self._mh.agg.unique_users(converted_users_filtered,
                                                             groupby=groupby_col)

        # remove double underscores from the columns name
        columns = {
            col: col[2:] if col.startswith('__') else col
            for col in groupby_col
        }
        _index = list(columns.values())
        converted_users_features = converted_users_features.reset_index().rename(columns=columns)
        converted_users_features = converted_users_features.dropna().set_index(_index)

        return converted_users_features.sort_values('unique_users', ascending=False)
