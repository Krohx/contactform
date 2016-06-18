"""
contact_form.db_ops
~~~~~~~~~~~~~~~~~~~

Database ORM Utilities.

Bunch of Utility functions for doing CRUD over ORM.

:author: Krohx Technologies (krohxinc@gmail.com)
:copyright: (c) 2016 by Krohx Technologies
:license: see LICENSE for details.
"""
from sqlalchemy.exc import IntegrityError

# local imports
from contact_form import db
from contact_form.models import Site, Message

# create database tables
#db.create_all()


# insert given record into specified table(model)
def insert_val(model, param_dict, commit=True, rollback_on_fail=True):
    """
    Inserts values of fields present in `param_dict` into a new row of
    the table `model` of the database.
    """
    row = model(**param_dict)
    db.session.add(row)
    if commit:
        try:
            commit_db()
        except IntegrityError:
            if rollback_on_fail:
                rollback()
            return False
    return True

# insert given list of values into specified table (model)
def insert_vals(model, dict_list, commit=True, rollback_on_fail=True):
    """
    Inserts values of fields present in each dict of `dict_list` into 
    new rows accordingly in the table `model` of the database.
    """
    errors = []
    for param_dict in dict_list:
        if not insert_val(model, param_dict, commit=commit, rollback_on_fail=rollback_on_fail):
            errors.append(param_dict)
    return errors


# update database with data
# :param: `model` DB table to be updated
# :param: `param_dict_ret` dict holding keyword args with which to
# retrieve previous data, before updation
# :param: `param_dict_ins` dict holding keyword args with which to
# insert new data
def update_row(model, param_dict_ret, param_dict_ins,  commit=True, rollback_on_fail=True):
    row = model.query.filter_by(**param_dict_ret).update(param_dict_ins)
    if commit:
        try:
            commit_db()
        except IntegrityError:
            if rollback_on_fail:
                rollback()
            return False
    return True


# Retreive record from specified table (model) using given key (for
# field) and value (as record)
def ret_val(model, param_dict):
    row = model.query.filter_by(**param_dict).first()
    return row


# Retreive records from specified table (model) using given key (for
# field) and value (as record)
def ret_all_val(model, param_dict, sort=None):
    if sort is None:
        row = model.query.filter_by(**param_dict).all()
    else:
        row = model.query.filter_by(**param_dict).order_by(*sort).all()
    return row


# Retreive all records from specified table (model)
def ret_all(model, sort=None):
    if sort is None:
        rows = model.query.all()
    else:
        rows = model.query.order_by(*sort).all()
    return rows


# Retrieve a pagination object of rowsthat can iterated
# over
def paginate(model, param_dict=None, sort=None, page=1, per_page=20, _404=True):

    if param_dict is not None:
        if sort is None:
            pagination_obj = model.query.filter_by(**param_dict).paginate(
                page=page, per_page=per_page, error_out=_404
            )
        else:
            pagination_obj = model.query.filter_by(**param_dict).order_by(*sort).paginate(
                page=page, per_page=per_page, error_out=_404
            )
    else:
        if sort is None:
            pagination_obj = model.query.paginate(
                page=page, per_page=per_page, error_out=_404
            )
        else:
            pagination_obj = model.query.order_by(*sort).paginate(
                page=page, per_page=per_page, error_out=_404
            )
    
    return pagination_obj


# commit changes to the database
def commit_db():
    db.session.commit()

# rollback changes
def rollback():
    db.session.rollback()