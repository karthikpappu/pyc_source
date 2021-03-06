# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/olek/Wszystkie_aggrescamy_swiata/aggrescan3d/a3d_gui/db_manager.py
# Compiled at: 2018-11-26 07:10:51
import sqlite3, os
from wtforms.validators import ValidationError
from flask import Response, request, flash, redirect, url_for
from a3d_gui import app
from utils import query_db, unique_id
from job_handling import delete_files, check_jobs
from create_config import reverse_config
from os.path import join, abspath, isfile
from parsePDB import PdbParser

def create_new_database(new_database):
    """Create an empty database that follows this apps schema"""
    try:
        try:
            conn = sqlite3.connect(new_database)
            c = conn.cursor()
            c.execute("CREATE TABLE user_queue (id INTEGER PRIMARY KEY, jid TEXT,\n                     status TEXT DEFAULT 'pending', project_name TEXT, working_dir TEXT,\n                     started DATETIME DEFAULT CURRENT_TIMESTAMP, pid INTEGER)")
            c.execute('CREATE TABLE project_details (jid TEXT, chains TEXT,\n                     chain_sequence TEXT, chain_numbering TEXT, dynamic INTEGER, mutate INTEGER, \n                     distance INTEGER, mutation TEXT, foldx INTEGER, mutt_energy_diff REAL,\n                     auto_mutation TEXT)')
            c.execute('CREATE TABLE pictures (jid TEXT, filename TEXT, type TEXT, model TEXT)')
            c.execute('CREATE TABLE system_data (id INTEGER PRIMARY KEY, foldx_path TEXT)')
            foldx_loc = raw_input('Please provide a location for your FoldX installation if you have one (or just press Enter this can be done later on)\n')
            conn.commit()
            try:
                try:
                    if os.path.isdir(foldx_loc):
                        if os.path.isfile(os.path.join(foldx_loc, 'rotabase.txt')):
                            c.execute('INSERT INTO system_data(foldx_path) VALUES(?)', [foldx_loc])
                        else:
                            c.execute('INSERT INTO system_data(foldx_path) VALUES(?)', ['Not specified'])
                            print '%s Is not a valid FoldX directory (missing rotabase.txt file). Use the gui to specify a valid location' % foldx_loc
                    else:
                        c.execute('INSERT INTO system_data(foldx_path) VALUES(?)', ['/home/FoldX'])
                        print '%s is not a directory. If you wish to use foldX in the gui specify a valid address when starting the job' % foldx_loc
                except EOFError:
                    c.execute('INSERT INTO system_data(foldx_path) VALUES(?)', [
                     '/home/FoldX'])

            finally:
                conn.commit()
                conn.close()

        except sqlite3.Error as e:
            raise ValidationError('An error occurred while trying to create a database: %s' % e)

    finally:
        conn.close()


@app.route('/_delete_job/<jid>', methods=['GET'])
def delete_job(jid):
    """Delete a job from current database"""
    try:
        query_db('DELETE FROM user_queue WHERE jid=?', [jid], insert=True)
        query_db('DELETE FROM project_details WHERE jid=?', [jid], insert=True)
        query_db('DELETE FROM pictures WHERE jid=?', [jid], insert=True)
        flash('Job %s deleted.' % jid, 'info')
        return url_for('index_page')
    except sqlite3.Error as e:
        return Response("The database couldn't process this request. Error: %s" % str(e), status=400, content_type='text/plain')


@app.route('/_hard_delete_job/<jid>', methods=['GET'])
def hard_delete_job(jid):
    """Delete a job from current database as well as the files from the computer"""
    try:
        folder_gone = delete_files(jid)
        query_db('DELETE FROM user_queue WHERE jid=?', [jid], insert=True)
        query_db('DELETE FROM project_details WHERE jid=?', [jid], insert=True)
        query_db('DELETE FROM pictures WHERE jid=?', [jid], insert=True)
        if folder_gone:
            flash('Job %s deleted. All files and the working directory were deleted.' % jid, 'info')
        else:
            flash('Job %s deleted. Aggrescan files were most likely deleted but the directory still contains files.' % jid, 'info')
        return url_for('index_page')
    except sqlite3.Error as e:
        return Response("The database couldn't process this request. Error: %s" % str(e), status=400, content_type='text/plain')


@app.route('/_add_job/', methods=['POST'])
def add_job_to_db():
    """Using a config file add a job to active database"""
    config_file = request.files['file']
    for line in config_file.stream.readlines():
        if 'work_dir :' in line:
            project_work_dir = line.split(':')[1].strip()

    try:
        options, mutation = reverse_config(join(project_work_dir, 'config.ini'))
    except UnboundLocalError:
        return Response("This file doesn't contain a working dir field which is necessary. Please select a valid config.ini file.", status=400, content_type='text/plain')

    jid = unique_id()
    if not isfile(join(project_work_dir, 'input.pdb')) and not isfile(join(project_work_dir, 'tmp', 'input.pdb')):
        return Response('This project has probably just started and some important files (input.pdb) are not yet created. Or have been deleted since. If its the former try again in a second.', status=400, content_type='text/plain')
    project_name = request.form['text'] or 'Custom project'
    mutate = 1 if mutation else 0
    dynamic = 1 if options['dynamic'] else 0
    foldx = 1 if options['foldx'] else 0
    auto_mutation = options['auto_mutation']
    query_db('INSERT INTO user_queue (jid, project_name, working_dir, pid)            VALUES(?,?,?,?)', [
     jid, project_name, project_work_dir, -100], insert=True)
    query_db('INSERT INTO project_details (jid, dynamic, mutate, distance, foldx, auto_mutation)              VALUES(?,?,?,?,?,?)', [
     jid, dynamic, mutate, options['distance'], foldx, auto_mutation], insert=True)
    try:
        with open(get_filepath(jid, 'input.pdb'), 'r') as (f):
            p = PdbParser(f, options['chain'])
    except IOError:
        with open(join(project_work_dir, 'tmp', 'input.pdb'), 'r') as (f):
            p = PdbParser(f, options['chain'])

    input_seq = p.getSequence()
    chain_numbering = p.getChainIdxResname()
    if not options['chain']:
        chains = p.getChains()
    query_db('UPDATE project_details SET chains=?, chain_sequence=?, chain_numbering=? WHERE jid=?', [
     ('').join(chains), input_seq, chain_numbering, jid], insert=True)
    check_jobs(jid)
    return url_for('job_status', jid=jid)


@app.route('/change_foldx_path', methods=['POST'])
def change_foldx_path():
    new_path = request.form['text']
    if not new_path:
        return Response('Empty path provided, not taking any action.', status=400, content_type='text/plain')
    if not isfile(join(new_path, 'rotabase.txt')):
        return Response('%s Is not a valid FoldX directory (missing rotabase.txt file).' % new_path, status=400, content_type='text/plain')
    query_db('UPDATE system_data SET foldx_path=? WHERE id=?', [new_path, 1], insert=True)
    return Response(new_path, status=200, content_type='text/plain')


@app.route('/_change_status/<jid>', methods=['POST'])
def change_job_status(jid):
    """Manually update a job status in case user wishes to do so"""
    new_status = request.data
    try:
        query_db('UPDATE user_queue SET status=? WHERE jid=?', [new_status, jid], insert=True)
        return Response('Query OK. Status changed to %s' % new_status, status=200, content_type='text/plain')
    except sqlite3.Error as e:
        return Response('Query failed! Error: %s' % str(e), status=400, content_type='text/plain')


def get_filepath(jid, filename):
    data_dir = query_db('SELECT working_dir FROM user_queue WHERE             jid=?', [jid], one=True)[0]
    return join(data_dir, filename)